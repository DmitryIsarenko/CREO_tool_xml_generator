"""Read user series without changing legacy catalog jobs."""

from collections.abc import Callable
import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from math import isfinite, pi
from pathlib import Path
import re
import tomllib
from xml.etree import ElementTree
from xml.sax.saxutils import escape

from src.tool_updater.classes.tool_classes.axial.counterbore import CounterBore
from src.tool_updater.classes.tool_classes.axial.countersink import CounterSink
from src.tool_updater.classes.tool_classes.axial.drill import Drill
from src.tool_updater.classes.tool_classes.axial.reamer import Reamer
from src.tool_updater.classes.tool_classes.axial.tap import (
    TapBlind,
    TapThrough,
)
from src.tool_updater.classes.tool_classes.base_tool import BaseTool
from src.tool_updater.classes.tool_classes.milling.endmill import EndMill
from src.tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from src.tool_updater.classes.tool_classes.milling.toroid_mill import (
    ToroidMill,
)
from src.tool_updater.config import PROJECT_DIR
from src.tool_updater.data_types import Catalog


SERIES_DIR = PROJECT_DIR / 'catalogs'
SETTINGS_FILE = PROJECT_DIR / 'settings' / 'machining.toml'
SETTINGS_FILES = {
    'ballmill': SETTINGS_FILE,
    'counterbore': PROJECT_DIR / 'settings' / 'counterbore.toml',
    'drill': PROJECT_DIR / 'settings' / 'drill.toml',
    'endmill': PROJECT_DIR / 'settings' / 'endmill.toml',
    'reamer': PROJECT_DIR / 'settings' / 'reamer.toml',
    'tap_blind': PROJECT_DIR / 'settings' / 'tap.toml',
    'tap_through': PROJECT_DIR / 'settings' / 'tap.toml',
    'toroidmill': PROJECT_DIR / 'settings' / 'toroidmill.toml',
    'countersink': PROJECT_DIR / 'settings' / 'countersink.toml',
}
SERIES_TYPES = tuple(SETTINGS_FILES)
MATERIALS = ('iso_P', 'iso_M', 'iso_K', 'iso_N', 'iso_S', 'iso_H')
GEOMETRY_COLUMNS = ('diameter_mm', 'flute_length_mm', 'length_mm', 'order_no')
DRILL_GEOMETRY_COLUMNS = (*GEOMETRY_COLUMNS, 'point_angle_deg')
COUNTERSINK_GEOMETRY_COLUMNS = (
    *GEOMETRY_COLUMNS,
    'point_diameter_mm',
    'point_angle_deg',
)
COUNTERBORE_GEOMETRY_COLUMNS = (
    *GEOMETRY_COLUMNS,
    'point_diameter_mm',
    'tip_offset_mm',
    'tail_holding_length_mm',
)
REAMER_GEOMETRY_COLUMNS = (
    *GEOMETRY_COLUMNS,
    'length_out_of_holder_mm',
    'corner_chamfer_mm',
)
TAP_GEOMETRY_COLUMNS = (
    *GEOMETRY_COLUMNS,
    'point_diameter_mm',
    'chamfer_length_mm',
    'thread_pitch_mm',
)
TOROIDMILL_GEOMETRY_COLUMNS = (*GEOMETRY_COLUMNS, 'corner_radius_mm')
CUTTING_COLUMNS = (
    'material',
    'diameter_mm',
    'vc_m_min',
    'feed_kind',
    'feed_value',
)


@dataclass(frozen=True)
class Series:
    """Describe one user-managed tool series."""

    directory: Path
    name: str
    tool_type: str
    teeth: int

    @property
    def identifier(self) -> str:
        """Return the directory identifier used by the CLI."""
        return self.directory.name


@dataclass(frozen=True)
class Machining:
    """Hold explicit settings for the existing calculation methods."""

    modes: dict[str, dict[str, float]]
    axial: dict[str, float]
    radial: dict[str, float]


def validate_identifier(identifier: str) -> None:
    """Reject unsafe or ambiguous directory identifiers."""
    reserved = {'con', 'prn', 'aux', 'nul'}
    reserved.update(
        f'{prefix}{n}' for prefix in ('com', 'lpt') for n in range(10)
    )
    if (
        not re.fullmatch(r'[a-z][a-z0-9_]{0,59}', identifier)
        or identifier in reserved
    ):
        raise ValueError(
            'Имя серии: от 1 до 60 символов a-z, 0-9 и _; '
            'первый символ — буква. Системные имена Windows запрещены.'
        )


def read_toml(path: Path) -> dict[str, object]:
    """Read a TOML file with path-aware syntax errors."""
    try:
        with path.open('rb') as source:
            return tomllib.load(source)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f'{path}: {exc}') from exc


def load_series(root: Path, identifier: str) -> Series:
    """Read and validate the public series description."""
    validate_identifier(identifier)
    directory = root / identifier
    path = directory / 'series.toml'
    data = read_toml(path)
    if set(data) != {'name', 'type', 'teeth'}:
        raise ValueError(f'{path}: нужны только поля name, type, teeth.')
    tool_type = data['type']
    if tool_type not in SERIES_TYPES:
        raise ValueError(
            f'{path}: type должен быть одним из {", ".join(SERIES_TYPES)}.'
        )
    name = data['name']
    teeth = data['teeth']
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f'{path}: name — непустое название серии.')
    if type(teeth) is not int or teeth <= 0:
        raise ValueError(f'{path}: teeth — целое число больше нуля.')
    return Series(directory, name, tool_type, teeth)


def _number(
    value: object, location: str, *, allow_zero: bool = False
) -> float:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f'{location}: нужно число.')
    try:
        number = float(
            value.replace(',', '.') if isinstance(value, str) else value
        )
    except ValueError as exc:
        raise ValueError(
            f'{location}: нужно число, получено {value!r}.'
        ) from exc
    if not isfinite(number) or number < 0 or (number == 0 and not allow_zero):
        limit = 'не меньше нуля' if allow_zero else 'больше нуля'
        raise ValueError(f'{location}: число должно быть конечным и {limit}.')
    return number


def _positive(value: object, location: str) -> float:
    """Read a finite number greater than zero."""
    return _number(value, location)


def load_machining(path: Path) -> Machining:
    """Validate every setting and reject unknown keys."""
    data = read_toml(path)
    expected = {'roughing', 'finishing', 'axial', 'radial'}
    if set(data) != expected:
        raise ValueError(
            f'{path}: нужны разделы {", ".join(sorted(expected))}.'
        )
    sections: dict[str, dict[str, float]] = {}
    for section in sorted(expected):
        values = data[section]
        keys = (
            {'vc_multiplier', 'feed_multiplier'}
            if section in {'roughing', 'finishing'}
            else set(MATERIALS)
        )
        if not isinstance(values, dict) or set(values) != keys:
            raise ValueError(
                f'{path}, [{section}]: нужны поля {sorted(keys)}.'
            )
        sections[section] = {}
        for key, value in values.items():
            location = f'{path}, [{section}].{key}'
            number = _number(value, location, allow_zero=section == 'radial')
            sections[section][key] = number
    modes = {
        mode: {
            'vc_modifier': sections[mode]['vc_multiplier'],
            'feed_rate_multiplier': sections[mode]['feed_multiplier'],
        }
        for mode in ('roughing', 'finishing')
    }
    return Machining(modes, sections['axial'], sections['radial'])


def _rows(
    path: Path, columns: tuple[str, ...]
) -> list[tuple[int, dict[str, str]]]:
    try:
        with path.open(encoding='utf-8-sig', newline='') as source:
            reader = csv.reader(source, delimiter=';', strict=True)
            header = next(reader, [])
            if header != list(columns):
                raise ValueError(
                    f'{path}: заголовок должен быть {";".join(columns)}'
                )
            result = []
            for row in reader:
                if not row:
                    continue
                if len(row) != len(columns):
                    raise ValueError(
                        f'{path}, строка {reader.line_num}: '
                        f'нужно {len(columns)} столбцов, разделитель — ;'
                    )
                result.append(
                    (reader.line_num, dict(zip(columns, row, strict=True)))
                )
    except csv.Error as exc:
        raise ValueError(f'{path}: ошибка CSV: {exc}') from exc
    if not result:
        raise ValueError(f'{path}: заполните хотя бы одну строку данных.')
    return result


def _diameter(value: str, location: str) -> str:
    _positive(value, location)
    try:
        diameter = Decimal(value.replace(',', '.'))
        if diameter != diameter.quantize(Decimal('0.01')):
            raise ValueError(
                f'{location}: поддерживаются до двух знаков после запятой.'
            )
    except InvalidOperation as exc:
        raise ValueError(f'{location}: недопустимый диаметр.') from exc
    return f'{diameter:.2f}'


def read_catalogs(series: Series) -> tuple[Catalog, Catalog]:
    """Convert checked CSV tables to the legacy calculation input."""
    geometry: Catalog = {}
    geometry_path = series.directory / 'geometry.csv'
    geometry_columns = {
        'counterbore': COUNTERBORE_GEOMETRY_COLUMNS,
        'drill': DRILL_GEOMETRY_COLUMNS,
        'countersink': COUNTERSINK_GEOMETRY_COLUMNS,
        'reamer': REAMER_GEOMETRY_COLUMNS,
        'tap_blind': TAP_GEOMETRY_COLUMNS,
        'tap_through': TAP_GEOMETRY_COLUMNS,
        'toroidmill': TOROIDMILL_GEOMETRY_COLUMNS,
    }
    columns = geometry_columns.get(series.tool_type, GEOMETRY_COLUMNS)
    for line, row in _rows(geometry_path, columns):
        location = f'{geometry_path}, строка {line}'
        diameter = _diameter(row['diameter_mm'], f'{location}, diameter_mm')
        if diameter in geometry:
            raise ValueError(
                f'{location}: диаметр {diameter} указан повторно.'
            )
        flute = _positive(
            row['flute_length_mm'], f'{location}, flute_length_mm'
        )
        length = _positive(row['length_mm'], f'{location}, length_mm')
        if flute >= length:
            raise ValueError(
                f'{location}: рабочая длина должна быть меньше общей.'
            )
        record: Catalog = {
            'flute_diam': float(diameter),
            'flute_len': flute,
            'full_body_len': length,
            'full_body_diam': float(diameter),
            'order_no': row['order_no'],
        }
        if series.tool_type == 'drill':
            point_angle = _positive(
                row['point_angle_deg'], f'{location}, point_angle_deg'
            )
            if point_angle >= 180:
                raise ValueError(
                    f'{location}, point_angle_deg: угол должен '
                    'быть меньше 180.'
                )
            record['point_angle'] = point_angle
        elif series.tool_type == 'countersink':
            point_diameter = _positive(
                row['point_diameter_mm'],
                f'{location}, point_diameter_mm',
            )
            if point_diameter >= float(diameter):
                raise ValueError(
                    f'{location}, point_diameter_mm: диаметр должен быть '
                    'меньше диаметра инструмента.'
                )
            point_angle = _positive(
                row['point_angle_deg'], f'{location}, point_angle_deg'
            )
            if point_angle >= 180:
                raise ValueError(
                    f'{location}, point_angle_deg: угол должен '
                    'быть меньше 180.'
                )
            if not point_angle.is_integer():
                raise ValueError(
                    f'{location}, point_angle_deg: нужен целый угол.'
                )
            record['point_diameter'] = point_diameter
            record['point_angle'] = int(point_angle)
        elif series.tool_type == 'counterbore':
            point_diameter = _positive(
                row['point_diameter_mm'],
                f'{location}, point_diameter_mm',
            )
            if point_diameter >= float(diameter):
                raise ValueError(
                    f'{location}, point_diameter_mm: диаметр должен быть '
                    'меньше диаметра инструмента.'
                )
            tip_offset = _positive(
                row['tip_offset_mm'], f'{location}, tip_offset_mm'
            )
            tail_holding_length = _positive(
                row['tail_holding_length_mm'],
                f'{location}, tail_holding_length_mm',
            )
            if tail_holding_length >= length:
                raise ValueError(
                    f'{location}, tail_holding_length_mm: длина должна '
                    'быть меньше общей длины.'
                )
            record['point_diameter'] = point_diameter
            record['point_len'] = tip_offset
            record['tail_for_hold'] = tail_holding_length
            record['cutter_diam'] = float(diameter)
        elif series.tool_type == 'reamer':
            length_out_of_holder = _positive(
                row['length_out_of_holder_mm'],
                f'{location}, length_out_of_holder_mm',
            )
            if length_out_of_holder > length:
                raise ValueError(
                    f'{location}, length_out_of_holder_mm: длина не может '
                    'быть больше общей длины.'
                )
            record['len_out_of_holder'] = length_out_of_holder
            record['corner_chamfer'] = _positive(
                row['corner_chamfer_mm'],
                f'{location}, corner_chamfer_mm',
            )
            record['teeth_num'] = series.teeth
        elif series.tool_type in {'tap_blind', 'tap_through'}:
            point_diameter = _positive(
                row['point_diameter_mm'],
                f'{location}, point_diameter_mm',
            )
            if point_diameter >= float(diameter):
                raise ValueError(
                    f'{location}, point_diameter_mm: диаметр должен быть '
                    'меньше диаметра инструмента.'
                )
            record['tapping_hole_diam'] = point_diameter
            record['chamfer_length'] = _positive(
                row['chamfer_length_mm'],
                f'{location}, chamfer_length_mm',
            )
            record['thread_pitch'] = _positive(
                row['thread_pitch_mm'], f'{location}, thread_pitch_mm'
            )
        elif series.tool_type == 'toroidmill':
            corner_radius = _positive(
                row['corner_radius_mm'], f'{location}, corner_radius_mm'
            )
            if corner_radius >= float(diameter) / 2:
                raise ValueError(
                    f'{location}, corner_radius_mm: радиус должен быть '
                    'меньше половины диаметра.'
                )
            record['corner_radius'] = corner_radius
        geometry[diameter] = record

    # Each diameter has its own Vc; legacy BallMill expects one Vc per catalog.
    cutting: Catalog = {}
    cutting_path = series.directory / 'cutting.csv'
    for line, row in _rows(cutting_path, CUTTING_COLUMNS):
        location = f'{cutting_path}, строка {line}'
        diameter = _diameter(row['diameter_mm'], f'{location}, diameter_mm')
        material = row['material'].strip()
        if diameter not in geometry:
            raise ValueError(
                f'{location}: диаметр {diameter} отсутствует в geometry.csv.'
            )
        if material not in MATERIALS:
            raise ValueError(
                f'{location}: material должен быть одним из {MATERIALS}.'
            )
        values = cutting.setdefault(diameter, {})
        if material in values:
            raise ValueError(f'{location}: повтор пары материал/диаметр.')
        speed = _positive(row['vc_m_min'], f'{location}, vc_m_min')
        feed = _positive(row['feed_value'], f'{location}, feed_value')
        kind = row['feed_kind'].strip()
        rpm = 1000 * speed / (pi * float(diameter))
        if kind not in {'F', 'Fz', 'Fn'}:
            raise ValueError(
                f'{location}: feed_kind должен быть F, Fz или Fn.'
            )
        if series.tool_type in {
            'counterbore',
            'drill',
            'countersink',
            'reamer',
            'tap_blind',
            'tap_through',
        }:
            if kind == 'F':
                feed /= rpm
            elif kind == 'Fz':
                feed *= series.teeth
            values[material] = {'Vc': speed, 'Fn': {diameter: feed}}
        else:
            if kind == 'Fz':
                feed *= rpm * series.teeth
            elif kind == 'Fn':
                feed *= rpm
            values[material] = {'Vc': speed, 'F': {diameter: feed}}
    for diameter in geometry:
        missing = set(MATERIALS) - set(cutting.get(diameter, {}))
        if missing:
            raise ValueError(
                f'{cutting_path}: для диаметра {diameter} нет групп '
                f'{", ".join(sorted(missing))}. '
                'Не подставляйте выдуманные режимы.'
            )
    return geometry, cutting


class SeriesBallMill(BallMill):
    """Build a user-managed ball mill."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


class SeriesDrill(Drill):
    """Build a user-managed drill."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


class SeriesCounterSink(CounterSink):
    """Build a user-managed countersink."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )
        self.point_angle = int(geometry[diameter]['point_angle'])
        self.set_tool_xml()

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


class SeriesCounterBore(CounterBore):
    """Build a user-managed counterbore."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )

    def set_xml_body_tool_params(self) -> str:
        """Write CSV point geometry omitted by the legacy standalone XML."""
        parameters = super().set_xml_body_tool_params()
        parameters = parameters.replace(
            'Name="POINT_DIAMETER" Value="0.0"',
            f'Name="POINT_DIAMETER" Value="{self.point_diameter}"',
        )
        return parameters.replace(
            'Name="TIP_OFFSET" Value="0.0"',
            f'Name="TIP_OFFSET" Value="{self.tip_offset}"',
        )


class SeriesReamer(Reamer):
    """Build a user-managed reamer."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


class SeriesTapBlind(TapBlind):
    """Build a user-managed blind-hole tap."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def get_chamfer_length(self) -> float:
        """Return the chamfer length entered in the CSV geometry row."""
        return float(
            self.catalog_tool_geometry[self.tool_size_from_geom_catalogue][
                'chamfer_length'
            ]
        )

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


class SeriesTapThrough(TapThrough):
    """Build a user-managed through-hole tap."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def get_chamfer_length(self) -> float:
        """Return the chamfer length entered in the CSV geometry row."""
        return float(
            self.catalog_tool_geometry[self.tool_size_from_geom_catalogue][
                'chamfer_length'
            ]
        )

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


class SeriesToroidMill(ToroidMill):
    """Build a user-managed toroid mill."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_flute_diam_from_complex_size(self) -> str:
        """Return the simple CSV diameter instead of a legacy compound key."""
        return self.complex_size_name

    def get_tool_corner_rad_from_complex_size(self) -> str:
        """Return the CSV corner radius for legacy XML assembly."""
        return str(
            self.catalog_tool_geometry[self.complex_size_name]['corner_radius']
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


class SeriesEndMill(EndMill):
    """Build a user-managed end mill."""

    def __init__(
        self,
        series: Series,
        geometry: Catalog,
        cutting: Catalog,
        diameter: str,
        machining: Machining,
    ) -> None:
        self.finishing_roughing_options = machining.modes
        self.axial_depth_modifiyers = machining.axial
        self.radial_depth_modifiyers = machining.radial
        super().__init__(
            tool_size_from_geom_catalogue=diameter,
            catalog_tool_cut_data=cutting,
            catalog_tool_geometry=geometry,
            teeth_num=series.teeth,
            file_name_prefix=f'{series.identifier}_',
            file_name_suffix='',
            debug_mode=0,
        )

    def get_tool_comment(self) -> str:
        """Escape a user comment before legacy XML interpolation."""
        return escape(super().get_tool_comment(), {'"': '&quot;'})

    def create_tool_name_for_xml(self) -> str:
        """Keep identifiers unique without legacy decimal normalization."""
        return (
            f'{self.tool_data["file_name_prefix"].upper()}'
            f'D{self.tool_data["tool_name_str"].replace(".", "-")}'
        )


ToolFactory = Callable[[Series, Catalog, Catalog, str, Machining], BaseTool]


TOOL_CLASSES: dict[str, ToolFactory] = {
    'ballmill': SeriesBallMill,
    'counterbore': SeriesCounterBore,
    'countersink': SeriesCounterSink,
    'drill': SeriesDrill,
    'endmill': SeriesEndMill,
    'reamer': SeriesReamer,
    'tap_blind': SeriesTapBlind,
    'tap_through': SeriesTapThrough,
    'toroidmill': SeriesToroidMill,
}


def prepare_tools(series: Series, machining: Machining) -> list[BaseTool]:
    """Validate all input, calculations and XML without writing files."""
    geometry, cutting = read_catalogs(series)
    tools: list[BaseTool] = []
    identifiers: set[str] = set()
    for diameter in geometry:
        try:
            tool = TOOL_CLASSES[series.tool_type](
                series, geometry, cutting[diameter], diameter, machining
            )
            if tool.tool_data['len_out_of_holder'] > tool.tool_data['LENGTH']:
                raise ValueError(
                    'Расчётный вылет больше общей длины инструмента.'
                )
            for material in tool.tool_data['cut_data'].values():
                for parameters in material.values():
                    for name, value in parameters.items():
                        allows_zero = name == 'TOOL_RADIAL_DEPTH' or (
                            name == 'TOOL_AXIAL_DEPTH'
                            and series.tool_type
                            in {'tap_blind', 'tap_through'}
                        )
                        if isinstance(value, (int, float)) and (
                            not isfinite(value)
                            or (value < 0)
                            or (not allows_zero and value == 0)
                        ):
                            raise ValueError(
                                f'{name}: недопустимый результат {value}.'
                            )
            tool.set_tool_xml()
            ElementTree.fromstring(tool.tool_xml)
            identifier = tool.tool_data['tool_name_for_xml'].casefold()
            if identifier in identifiers:
                raise ValueError('Повтор имени инструмента в XML.')
            identifiers.add(identifier)
        except (
            KeyError,
            TypeError,
            ValueError,
            ArithmeticError,
            ElementTree.ParseError,
        ) as exc:
            raise ValueError(
                f'{series.identifier}, диаметр {diameter}: {exc}'
            ) from exc
        tools.append(tool)
    return tools


def create_series(
    root: Path, identifier: str, tool_type: str = 'ballmill'
) -> Path:
    """Create empty tables; never supply synthetic machining parameters."""
    validate_identifier(identifier)
    if tool_type not in SERIES_TYPES:
        raise ValueError(f'Неизвестный type: {tool_type}.')
    directory = root / identifier
    directory.mkdir(parents=True, exist_ok=False)
    (directory / 'series.toml').write_text(
        '# Название серии и число зубьев замените своими значениями.\n'
        f'name = "Новая серия"\ntype = "{tool_type}"\nteeth = 0\n',
        encoding='utf-8',
    )
    for name, columns in (
        (
            'geometry.csv',
            {
                'counterbore': COUNTERBORE_GEOMETRY_COLUMNS,
                'drill': DRILL_GEOMETRY_COLUMNS,
                'countersink': COUNTERSINK_GEOMETRY_COLUMNS,
                'reamer': REAMER_GEOMETRY_COLUMNS,
                'tap_blind': TAP_GEOMETRY_COLUMNS,
                'tap_through': TAP_GEOMETRY_COLUMNS,
                'toroidmill': TOROIDMILL_GEOMETRY_COLUMNS,
            }.get(tool_type, GEOMETRY_COLUMNS),
        ),
        ('cutting.csv', CUTTING_COLUMNS),
    ):
        (directory / name).write_text(
            ';'.join(columns) + '\n', encoding='utf-8-sig'
        )
    (directory / 'source.txt').write_text(
        'Производитель:\nНазвание PDF:\nРедакция/дата:\n'
        'Страница размеров:\nСтраница режимов:\n'
        'Материал заготовки и условия применения режимов:\n',
        encoding='utf-8',
    )
    return directory
