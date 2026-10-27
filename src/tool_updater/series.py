"""Read user series without changing legacy catalog jobs."""

import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from math import isfinite, pi
from pathlib import Path
import re
import tomllib
from xml.etree import ElementTree
from xml.sax.saxutils import escape

from src.tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from src.tool_updater.config import PROJECT_DIR
from src.tool_updater.data_types import Catalog


SERIES_DIR = PROJECT_DIR / 'catalogs'
SETTINGS_FILE = PROJECT_DIR / 'settings' / 'machining.toml'
MATERIALS = ('iso_P', 'iso_M', 'iso_K', 'iso_N', 'iso_S', 'iso_H')
GEOMETRY_COLUMNS = ('diameter_mm', 'flute_length_mm', 'length_mm', 'order_no')
CUTTING_COLUMNS = (
    'material',
    'diameter_mm',
    'vc_m_min',
    'feed_kind',
    'feed_value',
)


@dataclass(frozen=True)
class Series:
    """Describe one user-managed ball mill series."""

    directory: Path
    name: str
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
    if data['type'] != 'ballmill':
        raise ValueError(
            f'{path}: пока поддерживается только type="ballmill".'
        )
    name = data['name']
    teeth = data['teeth']
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f'{path}: name — непустое название серии.')
    if type(teeth) is not int or teeth <= 0:
        raise ValueError(f'{path}: teeth — целое число больше нуля.')
    return Series(directory, name, teeth)


def _positive(value: object, location: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f'{location}: нужно положительное число.')
    try:
        number = float(
            value.replace(',', '.') if isinstance(value, str) else value
        )
    except ValueError as exc:
        raise ValueError(
            f'{location}: нужно число, получено {value!r}.'
        ) from exc
    if not isfinite(number) or number <= 0:
        raise ValueError(
            f'{location}: число должно быть конечным и больше нуля.'
        )
    return number


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
        sections[section] = {
            key: _positive(value, f'{path}, [{section}].{key}')
            for key, value in values.items()
        }
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
    for line, row in _rows(geometry_path, GEOMETRY_COLUMNS):
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
        geometry[diameter] = {
            'flute_diam': float(diameter),
            'flute_len': flute,
            'full_body_len': length,
            'full_body_diam': float(diameter),
            'order_no': row['order_no'],
        }

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
        if kind == 'Fz':
            feed *= rpm * series.teeth
        elif kind == 'Fn':
            feed *= rpm
        elif kind != 'F':
            raise ValueError(
                f'{location}: feed_kind должен быть F, Fz или Fn.'
            )
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
    """Use per-run settings without changing legacy class defaults."""

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


def prepare_tools(
    series: Series, machining: Machining
) -> list[SeriesBallMill]:
    """Validate all input, calculations and XML without writing files."""
    geometry, cutting = read_catalogs(series)
    tools = []
    identifiers: set[str] = set()
    for diameter in geometry:
        try:
            tool = SeriesBallMill(
                series, geometry, cutting[diameter], diameter, machining
            )
            if tool.tool_data['len_out_of_holder'] > tool.tool_data['LENGTH']:
                raise ValueError(
                    'Расчётный вылет больше общей длины инструмента.'
                )
            for material in tool.tool_data['cut_data'].values():
                for parameters in material.values():
                    for name, value in parameters.items():
                        if isinstance(value, (int, float)) and (
                            not isfinite(value) or value <= 0
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


def create_series(root: Path, identifier: str) -> Path:
    """Create empty tables; never supply synthetic machining parameters."""
    validate_identifier(identifier)
    directory = root / identifier
    directory.mkdir(parents=True, exist_ok=False)
    (directory / 'series.toml').write_text(
        '# Название серии и число зубьев замените своими значениями.\n'
        'name = "Новая серия"\ntype = "ballmill"\nteeth = 0\n',
        encoding='utf-8',
    )
    for name, columns in (
        ('geometry.csv', GEOMETRY_COLUMNS),
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
