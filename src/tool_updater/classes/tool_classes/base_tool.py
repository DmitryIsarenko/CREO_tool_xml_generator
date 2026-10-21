from copy import deepcopy
import datetime
import logging
from math import ceil, pi
from pathlib import Path
from typing import cast

from src.tool_updater import config
from src.tool_updater.config import key_f, key_fn, key_fz
from src.tool_updater.data_types import Catalog, ToolData
from src.tool_updater.default_tool_dict import default_tool_dict


logger = logging.getLogger(__name__)


class BaseTool:
    # BASIC DATA
    """Describe tool and holder parameters."""

    tool_file_extension = config.XML_EXTENSION
    DATETIME = datetime.datetime.today().strftime('%Y - %m-%dT%H:%M:%S')

    # MANUAL TOOL DATA
    tool_type = 'default tool type'
    tool_material_manual = 'HSS'

    holder_len_manual = '50.00'

    finishing_roughing_options: dict[str, dict[str, float]] = {
        'roughing': {
            'vc_modifier': 1,  # Множитель для подачи (и на зуб, и на оборот)
            'feed_rate_multiplier': 1,  # Множитель для скорости резания
        },
        'finishing': {
            'vc_modifier': 1.0,
            'feed_rate_multiplier': 1,
        },
    }

    axial_depth_modifiyers: dict[str, float] = {
        'iso_P': 1.0,
        'iso_M': 1.0,
        'iso_K': 1.0,
        'iso_N': 1.0,
        'iso_S': 1.0,
        'iso_H': 1.0,
    }
    radial_depth_modifiyers: dict[str, float] = {
        'iso_P': 0.1,
        'iso_M': 0.1,
        'iso_K': 0.1,
        'iso_N': 0.2,
        'iso_S': 0.1,
        'iso_H': 0.1,
    }

    def __init__(
        self,
        tool_size_from_geom_catalogue: str,
        catalog_tool_cut_data: Catalog,
        catalog_tool_geometry: Catalog,
        teeth_num: int,
        file_name_prefix: str,
        file_name_suffix: str,
        debug_mode: int,
        **kwargs: object,
    ) -> None:
        self.debug = debug_mode
        self.teeth_num = teeth_num
        if self.debug:
            self.finishing_roughing_options = {
                'roughing': {
                    # Множитель для подачи (и на зуб, и на оборот)
                    'vc_modifier': 1,
                    (
                        'feed_rate_multiplier'
                    ): 1,  # Множитель для скорости резания
                },
                'finishing': {
                    'vc_modifier': 1,
                    'feed_rate_multiplier': 1,
                },
            }
        # 0 Задаем первоначальную структуру словаря значений параметров
        # инструмента
        self.set_default_tool_data()

        # 1.1 Сохраняем имя инструмента в виде строки
        self.tool_data['tool_name_str'] = tool_size_from_geom_catalogue

        # 1.2 Сохраняем какие префиксы и суффиксы будут при имени файла
        self.tool_data['file_name_prefix'] = file_name_prefix
        self.tool_data['file_name_suffix'] = file_name_suffix

        # 1.3 Объявление каталогов
        self.catalog_geom = catalog_tool_geometry
        self.catalog_cut_data = catalog_tool_cut_data

        # 2.0 Независимые данные
        self.tool_data['HOLDER_LEN'] = self.get_holder_len()

        # 2.1 Создание данных, основанных на имени (диаметре) инструмента
        self.tool_data['tool_diam_float'] = self.get_tool_diam_float()
        self.tool_data['CUTTER_DIAM'] = self.get_cutter_diam()
        self.tool_data['cut_data_diam_group'] = self.calc_diam_group_name()
        self.tool_data['HOLDER_DIA'] = self.calc_nut_diam()

        # 2.2 Объявление имен, по которым будет совершаться поиск в каталогах
        self.tool_data['tool_name_for_geom_catalogue'] = (
            self.create_tool_name_for_geom_catalogue()
        )
        self.tool_data['tool_name_for_cut_catalogue'] = (
            self.create_tool_name_for_cut_catalogue()
        )

        # 3 Объявление переменных, используемых в XML
        self.tool_data['TOOL_MATERIAL'] = self.get_tool_material()
        self.tool_data['NUM_OF_TEETH'] = self.get_tool_teeth_num()
        self.tool_data['tool_type'] = self.get_tool_type()

        # 3.1 Получение данных из каталога геометрии
        self.tool_data['LENGTH'] = self.get_full_tool_length()
        self.tool_data['FLUTE_LENGTH'] = self.get_tool_flute_length()
        self.tool_data['TOOL_COMMENT'] = self.get_tool_comment()

        # 3.2 Создание данных, основанных на данных из каталога геометрии
        self.tool_data['len_out_of_holder'] = self.calc_len_out_of_holder()
        self.tool_data['tool_name_for_xml'] = self.create_tool_name_for_xml()
        self.tool_data['file_name'] = self.create_file_name()

        # 3.3 Расчет режимов резания для всех групп материалов
        self.calc_cut_data_for_all_material_groups()

        # 4 Генерация XML

    # GET FROM GEOM CATALOGUE
    def get_full_tool_length(self) -> float:
        """Return full tool length."""
        t_name = self.tool_data['tool_name_for_geom_catalogue']
        fractional_part = t_name.split('.')[1]
        if len(fractional_part) < 2:
            t_name += '0'
        return cast(float, self.catalog_geom[t_name][config.key_body_len])

    def get_tool_flute_length(self) -> float:
        """Return tool flute length."""
        t_name = self.tool_data['tool_name_for_geom_catalogue']
        fractional_part = t_name.split('.')[1]
        if len(fractional_part) < 2:
            t_name += '0'
        return cast(float, self.catalog_geom[t_name][config.key_flute_len])

    def get_tool_comment(self) -> str:
        """Return the optional catalog comment."""
        name = self.tool_data['tool_name_for_geom_catalogue']
        return cast(str, self.catalog_geom[name].get(config.key_order_no, ''))

    def get_tool_diam_float(self) -> float:
        """Return tool diam float."""
        return float(self.tool_data['tool_name_str'])

    def get_cutter_diam(self) -> float | str:
        """Return cutter diam."""
        return self.tool_data['tool_name_str']

    def get_holder_len(self) -> float | str:
        """Return holder len."""
        return self.holder_len_manual

    def get_tool_material(self) -> str:
        """Return tool material."""
        return self.tool_material_manual

    def get_tool_teeth_num(self) -> int:
        """Return tool teeth num."""
        return self.teeth_num

    def get_tool_type(self) -> str:
        """Return tool type."""
        return self.tool_type

    # GET FROM CUT DATA CATALOGUE
    def get_vc(self, key_iso_material: str, fin_or_rough: str) -> float:
        """Read surface speed for a supported material."""
        value = self.catalog_cut_data[key_iso_material][config.key_vc]
        modifier = self.finishing_roughing_options[fin_or_rough]['vc_modifier']
        if isinstance(value, (int, float)):
            return value * modifier
        if isinstance(value, (list, tuple)) and value:
            return cast(
                float,
                round(
                    value[config.vc_min_or_max] * modifier,
                    ndigits=config.NDIGITS_SURFACE_SPEED,
                ),
            )
        raise ValueError(f'Invalid surface speed for {key_iso_material}')

    # CALCULATIONS FOR GEOMETRY CATALOGUE
    def calc_diam_group_name(self) -> str:
        """Calculate diam group name."""
        iso_key = list(self.catalog_cut_data.keys())[0]
        cut_keys = list(self.catalog_cut_data[iso_key].keys())
        cut_key = key_fn
        for key in cut_keys:
            if key in [key_fn, key_f, key_fz]:
                cut_key = key
                break
        diam_groups = list(
            cast(dict[str, float], self.catalog_cut_data[iso_key][cut_key])
        )
        t_diam = self.tool_data['tool_diam_float']
        suitable_grp = []
        for grp_ind, grp in enumerate(diam_groups):
            grp_float = float(grp)
            if t_diam == grp_float:
                suitable_grp.append(grp)
                break
            elif t_diam > grp_float:
                suitable_grp.append(grp)
            elif t_diam < grp_float:
                if grp_ind == 0:
                    suitable_grp.append(grp)
                break
        return suitable_grp[-1]

    # CALCULATIONS FOR CUT DATA CATALOGUE
    def has_cutting_data(self, material: str) -> bool:
        """Return whether the catalog declares a material group."""
        return material in self.catalog_cut_data

    def calc_cut_data_for_all_material_groups(self) -> None:
        """Calculate cut data for all material groups."""
        for key_iso_material in config.lst_of_iso_material_groups:
            if not self.has_cutting_data(key_iso_material):
                logger.warning(
                    '%s: no cutting data for %s; defaults remain zero',
                    self.tool_data['tool_name_str'],
                    key_iso_material,
                )
                continue

            for fin_or_rough in self.finishing_roughing_options:
                tool_surface_speed = self.get_vc(
                    key_iso_material=key_iso_material,
                    fin_or_rough=fin_or_rough,
                )
                tool_spindle_rpm = self.calc_rpm(Vc=tool_surface_speed)

                self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                    'TOOL_SURFACE_SPEED'
                ] = tool_surface_speed
                self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                    'TOOL_SPINDLE_RPM'
                ] = tool_spindle_rpm

                tool_feed_per_unit = self.calc_feed_per_unit(
                    key_iso_material=key_iso_material,
                    fin_or_rough=fin_or_rough,
                )
                tool_feed_rate = self.calc_feed_rate(
                    key_iso_material=key_iso_material,
                    RPM=tool_spindle_rpm,
                    fin_or_rough=fin_or_rough,
                )
                tool_axial_depth = self.calc_axial_depth(
                    key_iso_material=key_iso_material
                )
                tool_radial_depth = self.calc_radial_depth(
                    key_iso_material=key_iso_material
                )

                multiplyer: float = 1
                if tool_spindle_rpm >= config.MAX_RPM:
                    multiplyer = config.MAX_RPM / tool_spindle_rpm
                    self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                        'TOOL_SPINDLE_RPM'
                    ] = round(
                        tool_spindle_rpm * multiplyer,
                        ndigits=config.NDIGITS_SPINDLE,
                    )
                    self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                        'TOOL_SURFACE_SPEED'
                    ] = round(
                        tool_surface_speed * multiplyer,
                        ndigits=config.NDIGITS_SURFACE_SPEED,
                    )

                self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                    'TOOL_FEED_PER_UNIT'
                ] = round(
                    tool_feed_per_unit * multiplyer,
                    ndigits=config.NDIGITS_FEED_PER_UNIT,
                )
                self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                    'TOOL_FEED_RATE'
                ] = round(
                    tool_feed_rate * multiplyer, ndigits=config.NDIGITS_FEED
                )
                self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                    'TOOL_AXIAL_DEPTH'
                ] = round(
                    tool_axial_depth * multiplyer,
                    ndigits=config.NDIGITS_AXIAL_FEED,
                )
                self.tool_data['cut_data'][key_iso_material][fin_or_rough][
                    'TOOL_RADIAL_DEPTH'
                ] = round(
                    tool_radial_depth * multiplyer,
                    ndigits=config.NDIGITS_RADIAL_FEED,
                )

        for non_iso_key in config.lst_of_not_iso_material_groups:
            for fin_or_rough in self.finishing_roughing_options:
                from_iso = config.not_iso_materials_modifyers[non_iso_key][
                    'from_iso'
                ]
                k_Vc = config.not_iso_materials_modifyers[non_iso_key]['k_Vc']
                k_Ae = config.not_iso_materials_modifyers[non_iso_key]['k_Ae']
                k_Ap = config.not_iso_materials_modifyers[non_iso_key]['k_Ap']
                k_Fz = config.not_iso_materials_modifyers[non_iso_key]['k_Fz']

                self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                    'TOOL_SPINDLE_RPM'
                ] = round(
                    cast(
                        float,
                        self.tool_data['cut_data'][from_iso][fin_or_rough][
                            'TOOL_SPINDLE_RPM'
                        ],
                    )
                    * k_Vc,
                    ndigits=config.NDIGITS_SPINDLE,
                )

                self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                    'TOOL_SURFACE_SPEED'
                ] = round(
                    cast(
                        float,
                        self.tool_data['cut_data'][from_iso][fin_or_rough][
                            'TOOL_SURFACE_SPEED'
                        ],
                    )
                    * k_Vc,
                    ndigits=config.NDIGITS_SURFACE_SPEED,
                )

                self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                    'TOOL_FEED_PER_UNIT'
                ] = round(
                    cast(
                        float,
                        self.tool_data['cut_data'][from_iso][fin_or_rough][
                            'TOOL_FEED_PER_UNIT'
                        ],
                    )
                    * k_Fz,
                    ndigits=config.NDIGITS_FEED_PER_UNIT,
                )

                self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                    'TOOL_FEED_RATE'
                ] = round(
                    cast(
                        float,
                        self.tool_data['cut_data'][from_iso][fin_or_rough][
                            'TOOL_FEED_RATE'
                        ],
                    )
                    * k_Fz,
                    ndigits=config.NDIGITS_FEED,
                )

                self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                    'TOOL_AXIAL_DEPTH'
                ] = round(
                    cast(
                        float,
                        self.tool_data['cut_data'][from_iso][fin_or_rough][
                            'TOOL_AXIAL_DEPTH'
                        ],
                    )
                    * k_Ap,
                    ndigits=config.NDIGITS_AXIAL_FEED,
                )

                self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                    'TOOL_RADIAL_DEPTH'
                ] = round(
                    cast(
                        float,
                        self.tool_data['cut_data'][from_iso][fin_or_rough][
                            'TOOL_RADIAL_DEPTH'
                        ],
                    )
                    * k_Ae,
                    ndigits=config.NDIGITS_RADIAL_FEED,
                )

        for non_iso_key in ['iso_H', 'iso_S']:
            for fin_or_rough in self.finishing_roughing_options:
                if (
                    self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                        'TOOL_SPINDLE_RPM'
                    ]
                    == 0
                ):
                    from_iso = config.not_iso_materials_modifyers[non_iso_key][
                        'from_iso'
                    ]
                    k_Vc = config.not_iso_materials_modifyers[non_iso_key][
                        'k_Vc'
                    ]
                    k_Ae = config.not_iso_materials_modifyers[non_iso_key][
                        'k_Ae'
                    ]
                    k_Ap = config.not_iso_materials_modifyers[non_iso_key][
                        'k_Ap'
                    ]
                    k_Fz = config.not_iso_materials_modifyers[non_iso_key][
                        'k_Fz'
                    ]

                    self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                        'TOOL_SPINDLE_RPM'
                    ] = round(
                        cast(
                            float,
                            self.tool_data['cut_data'][from_iso][fin_or_rough][
                                'TOOL_SPINDLE_RPM'
                            ],
                        )
                        * k_Vc,
                        ndigits=config.NDIGITS_SPINDLE,
                    )

                    self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                        'TOOL_SURFACE_SPEED'
                    ] = round(
                        cast(
                            float,
                            self.tool_data['cut_data'][from_iso][fin_or_rough][
                                'TOOL_SURFACE_SPEED'
                            ],
                        )
                        * k_Vc,
                        ndigits=config.NDIGITS_SURFACE_SPEED,
                    )

                    self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                        'TOOL_FEED_PER_UNIT'
                    ] = round(
                        cast(
                            float,
                            self.tool_data['cut_data'][from_iso][fin_or_rough][
                                'TOOL_FEED_PER_UNIT'
                            ],
                        )
                        * k_Fz,
                        ndigits=config.NDIGITS_FEED_PER_UNIT,
                    )

                    self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                        'TOOL_FEED_RATE'
                    ] = round(
                        cast(
                            float,
                            self.tool_data['cut_data'][from_iso][fin_or_rough][
                                'TOOL_FEED_RATE'
                            ],
                        )
                        * k_Fz,
                        ndigits=config.NDIGITS_FEED,
                    )

                    self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                        'TOOL_AXIAL_DEPTH'
                    ] = round(
                        cast(
                            float,
                            self.tool_data['cut_data'][from_iso][fin_or_rough][
                                'TOOL_AXIAL_DEPTH'
                            ],
                        )
                        * k_Ap,
                        ndigits=config.NDIGITS_AXIAL_FEED,
                    )

                    self.tool_data['cut_data'][non_iso_key][fin_or_rough][
                        'TOOL_RADIAL_DEPTH'
                    ] = round(
                        cast(
                            float,
                            self.tool_data['cut_data'][from_iso][fin_or_rough][
                                'TOOL_RADIAL_DEPTH'
                            ],
                        )
                        * k_Ae,
                        ndigits=config.NDIGITS_RADIAL_FEED,
                    )

    def calc_rpm(self, Vc: int | float) -> float:
        """Calculate rpm."""
        rpm = 1000 * Vc / (pi * self.tool_data['tool_diam_float'])
        return round(rpm, ndigits=config.NDIGITS_SPINDLE)

    def calc_feed_per_unit(
        self, key_iso_material: str, fin_or_rough: str
    ) -> float:
        """Calculate feed per unit."""
        feed_multiplier = self.finishing_roughing_options[fin_or_rough][
            'feed_rate_multiplier'
        ]
        F = self.catalog_cut_data[key_iso_material][config.key_f][
            self.tool_data['cut_data_diam_group']
        ]
        RPM = self.tool_data['cut_data'][key_iso_material][fin_or_rough][
            'TOOL_SPINDLE_RPM'
        ]
        fz = F / RPM / self.tool_data['NUM_OF_TEETH'] * feed_multiplier
        return cast(float, round(fz, ndigits=config.NDIGITS_FEED_PER_UNIT))

    def calc_feed_rate(
        self, key_iso_material: str, RPM: float, fin_or_rough: str
    ) -> float:
        """Calculate feed rate."""
        Fn = self.catalog_cut_data[key_iso_material][config.key_fn][
            self.tool_data['cut_data_diam_group']
        ]
        feed_multiplier = self.finishing_roughing_options[fin_or_rough][
            'feed_rate_multiplier'
        ]
        Fn = Fn * RPM * feed_multiplier
        return cast(float, round(Fn, ndigits=config.NDIGITS_FEED))

    def calc_axial_depth(self, key_iso_material: str) -> float:
        """Calculate axial depth."""
        axial_depth = (
            float(self.tool_data['CUTTER_DIAM'])
            * self.axial_depth_modifiyers[key_iso_material]
        )
        return round(axial_depth, ndigits=config.NDIGITS_AXIAL_FEED)

    def calc_radial_depth(self, key_iso_material: str) -> float:
        """Calculate radial depth."""
        radial_depth = (
            float(self.tool_data['CUTTER_DIAM'])
            * self.radial_depth_modifiyers[key_iso_material]
        )
        return round(radial_depth, ndigits=config.NDIGITS_RADIAL_FEED)

    def calc_nut_diam(self) -> float:
        """Calculate nut diam."""
        cut_d = float(self.tool_data['CUTTER_DIAM'])
        nut_diam = 0
        for er in config.collet_sizes:
            max_d: int = config.collet_sizes[er]['max_diam']
            if cut_d <= max_d:
                nut_diam = config.collet_sizes[er]['nut_diam']
                break
            else:
                continue
        return nut_diam

    def calc_len_out_of_holder(self) -> float:
        """Calculate len out of holder."""
        length = round(
            float(self.tool_data['FLUTE_LENGTH'])
            + float(self.tool_data['CUTTER_DIAM']),
            ndigits=0,
        )
        return length

    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA
    def create_tool_name_for_geom_catalogue(self) -> str:
        """Create tool name for geom catalogue."""
        t_name = self.tool_data['tool_name_str']
        return t_name

    def create_tool_name_for_cut_catalogue(self) -> float | str:
        """Create tool name for cut catalogue."""
        t_name = self.tool_data['tool_diam_float']
        return t_name

    def create_tool_name_for_xml(self) -> str:
        """Create tool name for xml."""
        t_prefix = self.tool_data['file_name_prefix'].upper()
        _t_suffix = self.tool_data['file_name_suffix'].upper()

        d = self.clear_str_from_trailing_zeros(
            str(self.tool_data['CUTTER_DIAM']), sep='.'
        ).replace('.', '-')
        l1 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['FLUTE_LENGTH']), sep='.'
        ).replace('.', '-')
        l2 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['LENGTH']), sep='.'
        ).replace('.', '-')

        t_name = f'{t_prefix}D{d}_L{l1}_L{l2}'
        return t_name

    def create_file_name(self) -> str:
        """Create file name."""
        t_prefix = self.tool_data['file_name_prefix']
        t_suffix = self.tool_data['file_name_suffix']

        d = self.clear_str_from_trailing_zeros(
            str(self.tool_data['CUTTER_DIAM']), sep='.'
        )
        l1 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['FLUTE_LENGTH']), sep='.'
        )
        l2 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['LENGTH']), sep='.'
        )

        t_name = f'{t_prefix}D{d}_L{l1}_L{l2}{t_suffix}'
        return t_name

    @staticmethod
    def clear_str_from_trailing_zeros(str_to_clean: str, sep: str) -> str:
        """Format the size string with the existing zero removal rule."""
        new_str = str_to_clean.split(sep=sep)[0]
        try:
            rev_str_pt2 = str_to_clean.split('.')[1][::-1]
            rev_new_pt = ''
            for _ch_i, char in enumerate(rev_str_pt2):
                if char != '0':
                    rev_new_pt += char
                else:
                    continue
            if rev_new_pt:
                new_str += sep + rev_new_pt[::-1]
        except IndexError:
            pass
        return new_str

    # FILE OPERATIONS

    def write_new_file(
        self,
        path: str | Path,
        *,
        overwrite: bool = False,
    ) -> None:
        """Write tool XML and let the caller handle file errors."""
        file_name = f'{self.tool_data["file_name"]}{self.tool_file_extension}'
        output_file = Path(path) / file_name
        mode = 'w' if overwrite else 'x'
        with output_file.open(mode, encoding=config.TEXT_ENCODING) as file:
            file.write(self.tool_xml)

    # DEFAULT TOOL DICT
    def set_default_tool_data(self) -> None:
        """Set default tool data."""
        self.tool_data = cast(ToolData, deepcopy(default_tool_dict))

    # XML DEFINITION
    def set_tool_xml(self) -> None:
        """Set tool xml."""
        if self.debug == 0:
            self.tool_xml = ''
            self.tool_xml += self.set_xml_head()
            self.tool_xml += self.set_xml_body_tool_params()
            self.tool_xml += self.set_xml_body_tool_cut_data()
            self.tool_xml += self.set_xml_bom_components()
            self.tool_xml += self.set_xml_tail()
        elif self.debug == 1:
            self.tool_xml = (
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<DateTime>'
                f'{self.DATETIME}'
                '</DateTime>\n'
                '<Tool Id="'
                f'{self.tool_data["tool_name_for_xml"]}'
                '" RefXmlId="encref_1" Type="'
                f'{self.tool_data["tool_type"]}'
                '">\n'
                '\n'
                'Общие:\n'
                '    "GAUGE_X_LENGTH": "'
                f'{self.tool_data["GAUGE_X_LENGTH"]}'
                '",\n'
                '    "GAUGE_Z_LENGTH": "'
                f'{self.tool_data["GAUGE_Z_LENGTH"]}'
                '",\n'
                '    "LENGTH_UNITS": "'
                f'{self.tool_data["LENGTH_UNITS"]}'
                '",\n'
                '    "TOOL_MATERIAL": '
                f'{self.tool_data["TOOL_MATERIAL"]}'
                ',\n'
                '    "TOOL_COMMENT": '
                f'{self.tool_data["TOOL_COMMENT"]}'
                ',\n'
                '    "SPINDLE_SENSE": "'
                f'{self.tool_data["SPINDLE_SENSE"]}'
                '",\n'
                '    "COOLANT_OPTION": "'
                f'{self.tool_data["COOLANT_OPTION"]}'
                '",\n'
                '    "COOLANT_PRESSURE": "'
                f'{self.tool_data["COOLANT_PRESSURE"]}'
                '",\n'
                '# геометрия\n'
                '    "CUTTER_DIAM": '
                f'{self.tool_data["CUTTER_DIAM"]}'
                ',\n'
                '    "CORNER_RADIUS": '
                f'{self.tool_data["CORNER_RADIUS"]}'
                '"\n'
                '    "NUM_OF_TEETH": '
                f'{self.tool_data["NUM_OF_TEETH"]}'
                ',\n'
                '    "HOLDER_DIA": '
                f'{self.tool_data["HOLDER_DIA"]}'
                ',\n'
                '    "HOLDER_LEN": '
                f'{self.tool_data["HOLDER_LEN"]}'
                ',\n'
                '    "LENGTH": '
                f'{self.tool_data["LENGTH"]}'
                ',\n'
                '    "FLUTE_LENGTH": '
                f'{self.tool_data["FLUTE_LENGTH"]}'
                ',\n'
                '    "len_out_of_holder": '
                f'{self.tool_data["len_out_of_holder"]}'
                ',\n'
                '    "cut_data_diam_group": '
                f'{self.tool_data["cut_data_diam_group"]}'
                ',\n'
                '# фрезы\n'
                '# фрезы тороидальные\n'
                '    "CORNER_RADIUS": '
                f'{self.tool_data["CORNER_RADIUS"]}'
                ',\n'
                '# сверла\n'
                '# центровки\n'
                '    "POINT_ANGLE": '
                f'{self.tool_data["POINT_ANGLE"]}'
                ',\n'
                '    "CSINK_ANGLE": '
                f'{self.tool_data["CSINK_ANGLE"]}'
                ',\n'
                '# резьбофрезы\n'
                '    "INSERT_LENGTH": '
                f'{self.tool_data["INSERT_LENGTH"]}'
                ',\n'
                '    "END_OFFSET": '
                f'{self.tool_data["END_OFFSET"]}'
                ',\n'
                '# не сортированное\n'
                '    "SIDE_ANGLE": '
                f'{self.tool_data["SIDE_ANGLE"]}'
                ',\n'
                '    "TOOL_LONG_FLAG": '
                f'{self.tool_data["TOOL_LONG_FLAG"]}'
                ',\n'
                '    "CUT_LENGTH": '
                f'{self.tool_data["CUT_LENGTH"]}'
                ',\n'
                '    "TIP_LENGTH": '
                f'{self.tool_data["TIP_LENGTH"]}'
                ',\n'
                '    "SHANK_DIAM": '
                f'{self.tool_data["SHANK_DIAM"]}'
                ',\n'
                '    "COMP_OVERSIZE": '
                f'{self.tool_data["COMP_OVERSIZE"]}'
                ',\n'
                '    "DRILL_DIAMETER": '
                f'{self.tool_data["DRILL_DIAMETER"]}'
                ',\n'
                '    "DRILL_LENGTH": '
                f'{self.tool_data["DRILL_LENGTH"]}'
                ',\n'
                '    "CHAMFER_LENGTH": '
                f'{self.tool_data["CHAMFER_LENGTH"]}'
                ',\n'
            )

        elif self.debug == 2:
            self.tool_xml = (
                '            <?xml version="1.0" encoding="UTF'
                '-8"?>\n'
                '            <Tool Id="'
                f'{self.tool_data["tool_name_for_xml"]}'
                '" RefXmlId="encref_1" Type="'
                f'{self.tool_data["tool_type"]}'
                '">\n'
                '\n'
                '            "STEEL-20"/>\n'
                '                "ROUGHING"/>\n'
                '                    "TOOL_SURFACE_SPEED" = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_SURFACE_SPEED"]}'
                '\n'
                '                    "TOOL_SPINDLE_RPM" =   '
                f'{self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_SPINDLE_RPM"]}'
                '\n'
                '                    "TOOL_FEED_PER_UNIT" = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_FEED_PER_UNIT"]}'
                '\n'
                '                    "TOOL_FEED_RATE" =     '
                f'{self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_FEED_RATE"]}'
                '\n'
                '                    "TOOL_AXIAL_DEPTH" =   '
                f'{self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_AXIAL_DEPTH"]}'
                '\n'
                '                    "TOOL_RADIAL_DEPTH"  = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["roughing"]["TOOL_RADIAL_DEPTH"]}'
                '\n'
                '                "FINISHING"/>\n'
                '                    "TOOL_SURFACE_SPEED" = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_SURFACE_SPEED"]}'
                '\n'
                '                    "TOOL_SPINDLE_RPM"   = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_SPINDLE_RPM"]}'
                '\n'
                '                    "TOOL_FEED_PER_UNIT" = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_FEED_PER_UNIT"]}'
                '\n'
                '                    "TOOL_FEED_RATE"     = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_FEED_RATE"]}'
                '\n'
                '                    "TOOL_AXIAL_DEPTH"   = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_AXIAL_DEPTH"]}'
                '\n'
                '                    "TOOL_RADIAL_DEPTH"  = '
                f'{self.tool_data["cut_data"][config.key_iso_P]["finishing"]["TOOL_RADIAL_DEPTH"]}'
                '\n'
                '\n'
                '            "12X18H10T"/>\n'
                '                "ROUGHING"/>\n'
                '                    "TOOL_SURFACE_SPEED" = '
                f'{self.tool_data["cut_data"][config.key_iso_M]["roughing"]["TOOL_SURFACE_SPEED"]}'
                '\n'
                '                    "TOOL_SPINDLE_RPM" =   '
                f'{self.tool_data["cut_data"][config.key_iso_M]["roughing"]["TOOL_SPINDLE_RPM"]}'
                '\n'
                '                    "TOOL_FEED_PER_UNIT" = '
                f'{self.tool_data["cut_data"][config.key_iso_M]["roughing"]["TOOL_FEED_PER_UNIT"]}'
                '\n'
                '                    "TOOL_FEED_RATE" =     '
                f'{self.tool_data["cut_data"][config.key_iso_M]["roughing"]["TOOL_FEED_RATE"]}'
                '\n'
                '                    "TOOL_AXIAL_DEPTH" =   '
                f'{self.tool_data["cut_data"][config.key_iso_M]["roughing"]["TOOL_AXIAL_DEPTH"]}'
                '\n'
                '                    "TOOL_RADIAL_DEPTH"  = '
                f'{self.tool_data["cut_data"][config.key_iso_M]["roughing"]["TOOL_RADIAL_DEPTH"]}'
                '\n'
                '                "FINISHING"/>\n'
                '                    "TOOL_SURFACE_SPEED" = '
                f'{self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_SURFACE_SPEED"]}'
                '\n'
                '                    "TOOL_SPINDLE_RPM" =   '
                f'{self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_SPINDLE_RPM"]}'
                '\n'
                '                    "TOOL_FEED_PER_UNIT" = '
                f'{self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_FEED_PER_UNIT"]}'
                '\n'
                '                    "TOOL_FEED_RATE" =     '
                f'{self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_FEED_RATE"]}'
                '\n'
                '                    "TOOL_AXIAL_DEPTH" =   '
                f'{self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_AXIAL_DEPTH"]}'
                '\n'
                '                    "TOOL_RADIAL_DEPTH"  = '
                f'{self.tool_data["cut_data"][config.key_iso_M]["finishing"]["TOOL_RADIAL_DEPTH"]}'
                '\n'
                '\n'
                '            "ALUMINIUM"/>\n'
                '                "ROUGHING"/>\n'
                '                    "TOOL_SURFACE_SPEED" = '
                f'{self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_SURFACE_SPEED"]}'
                '\n'
                '                    "TOOL_SPINDLE_RPM" =   '
                f'{self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_SPINDLE_RPM"]}'
                '\n'
                '                    "TOOL_FEED_PER_UNIT" = '
                f'{self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_FEED_PER_UNIT"]}'
                '\n'
                '                    "TOOL_FEED_RATE" =     '
                f'{self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_FEED_RATE"]}'
                '\n'
                '                    "TOOL_AXIAL_DEPTH" =   '
                f'{self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_AXIAL_DEPTH"]}'
                '\n'
                '                    "TOOL_RADIAL_DEPTH"  = '
                f'{self.tool_data["cut_data"][config.key_iso_N]["roughing"]["TOOL_RADIAL_DEPTH"]}'
                '\n'
                '                "FINISHING"/>\n'
                '                    "TOOL_SURFACE_SPEED" = '
                f'{self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_SURFACE_SPEED"]}'
                '\n'
                '                    "TOOL_SPINDLE_RPM" =   '
                f'{self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_SPINDLE_RPM"]}'
                '\n'
                '                    "TOOL_FEED_PER_UNIT" = '
                f'{self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_FEED_PER_UNIT"]}'
                '\n'
                '                    "TOOL_FEED_RATE" =     '
                f'{self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_FEED_RATE"]}'
                '\n'
                '                    "TOOL_AXIAL_DEPTH" =   '
                f'{self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_AXIAL_DEPTH"]}'
                '\n'
                '                    "TOOL_RADIAL_DEPTH"  = '
                f'{self.tool_data["cut_data"][config.key_iso_N]["finishing"]["TOOL_RADIAL_DEPTH"]}'
                '\n'
                '            '
            )

    def set_xml_head(self) -> str:
        """Set xml head."""
        xml_part_str = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<MfgSetupDocument>\n'
            '    <DocType>PRO_NC_CUTTING_TOOL_SETUP</DocTy'
            'pe>\n'
            '    <DocTitle>Инфо режущего инструмента</DocT'
            'itle>\n'
            '    <DateTime>'
            f'{self.DATETIME}'
            '</DateTime>\n'
            '    <ApplicationInfo AppName="Creo" AppVersio'
            'n="8.0.11.0" FtVersion="360051" Language="rus'
            'sian" MdlVersion="2012"/>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]} - xml_head generated...'
        )
        return xml_part_str

    def set_xml_body_tool_params(self) -> str:
        """Set xml body tool params."""
        xml_part_str = (
            '    <ToolingSetup>\n'
            '        <Tool Id="'
            f'{self.tool_data["tool_name_for_xml"]}'
            '" RefXmlId="encref_1" Type="'
            f'{self.tool_data["tool_type"]}'
            '">\n'
            '            <Attr DataType="boolean" Name="Us'
            'eOutline" Value="false"/>\n'
            '            <Attr DataType="boolean" Name="Pr'
            'oLibraryTool" Value="false"/>\n'
            '            <Attr DataType="boolean" Name="Sk'
            'etchTool" Value="false"/>\n'
            '            <Attr DataType="boolean" Name="To'
            'olByRef" Value="false"/>\n'
            '            <MfgParam Name="LENGTH_UNITS" Val'
            'ue="'
            f'{self.tool_data["LENGTH_UNITS"]}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_DIAM" Valu'
            'e="'
            f'{self.tool_data["CUTTER_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="LENGTH" Value="'
            f'{self.tool_data["len_out_of_holder"]}'
            '"/>\n'
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
            '"/>\n'
            '            <MfgParam Name="GAUGE_X_LENGTH" V'
            'alue="'
            f'{self.tool_data["GAUGE_X_LENGTH"]}'
            '"/>\n'
            '            <MfgParam Name="GAUGE_Z_LENGTH" V'
            'alue="'
            f'{self.tool_data["GAUGE_Z_LENGTH"]}'
            '"/>\n'
            '            <MfgParam Name="COMP_OVERSIZE" Va'
            'lue="'
            f'{self.tool_data["COMP_OVERSIZE"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_LONG_FLAG" V'
            'alue="'
            f'{self.tool_data["TOOL_LONG_FLAG"]}'
            '"/>\n'
            '            <MfgParam Name="HOLDER_DIA" Value'
            '="'
            f'{self.tool_data["HOLDER_DIA"]}'
            '"/>\n'
            '            <MfgParam Name="HOLDER_LEN" Value'
            '="'
            f'{self.tool_data["HOLDER_LEN"]}'
            '"/>\n'
            '            <MfgParam Name="COOLANT_OPTION" V'
            'alue="'
            f'{self.tool_data["COOLANT_OPTION"]}'
            '"/>\n'
            '            <MfgParam Name="COOLANT_PRESSURE"'
            ' Value="'
            f'{self.tool_data["COOLANT_PRESSURE"]}'
            '"/>\n'
            '            <MfgParam Name="SPINDLE_SENSE" Va'
            'lue="'
            f'{self.tool_data["SPINDLE_SENSE"]}'
            '"/>\n'
            '            <MfgParam Name="FLUTE_LENGTH" Val'
            'ue="'
            f'{self.tool_data["FLUTE_LENGTH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]} - xml_tool_params generated...'
        )
        return xml_part_str

    def set_xml_body_tool_cut_data(self) -> str:
        """Set xml body tool cut data."""
        total_string = ''
        for material_name, mat_iso_name in config.mfg_materials_dict.items():
            xml_part_str = (
                '        <ToolCutData>\n'
                '                <Material>\n'
                '                    <MfgParam Name="STOCK_MAT'
                'ERIAL" Value="'
                f'{material_name}'
                '"/>\n'
                '                </Material>\n'
                '                <CutDataUnitSystem>\n'
                '                    <MfgParam Name="CUT_DATA_'
                'UNITS" Value="METRIC"/>\n'
                '                </CutDataUnitSystem>\n'
                '                <Technology>\n'
                '                    <Condition>\n'
                '                        <MfgParam Name="APPLI'
                'CATION_TYPE" Value="ROUGHING"/>\n'
                '                    </Condition>\n'
                '                    <MfgParam Name="TOOL_SPIN'
                'DLE_RPM" Unit="rev_per_min" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_SPINDLE_RPM"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_SURF'
                'ACE_SPEED" Unit="m_per_min" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_SURFACE_SPEED"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_FEED'
                '_RATE" Unit="mm_per_min" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_RATE"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_FEED'
                '_PER_UNIT" Unit="mm_per_tooth" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_PER_UNIT"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_AXIA'
                'L_DEPTH" Unit="mm" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_AXIAL_DEPTH"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_RADI'
                'AL_DEPTH" Unit="mm" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_RADIAL_DEPTH"]}'
                '"/>\n'
                '                </Technology>\n'
                '                <Technology>\n'
                '                    <Condition>\n'
                '                        <MfgParam Name="APPLI'
                'CATION_TYPE" Value="FINISHING"/>\n'
                '                    </Condition>\n'
                '                    <MfgParam Name="TOOL_SPIN'
                'DLE_RPM" Unit="rev_per_min" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SPINDLE_RPM"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_SURF'
                'ACE_SPEED" Unit="m_per_min" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SURFACE_SPEED"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_FEED'
                '_RATE" Unit="mm_per_min" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_RATE"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_FEED'
                '_PER_UNIT" Unit="mm_per_tooth" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_PER_UNIT"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_AXIA'
                'L_DEPTH" Unit="mm" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_AXIAL_DEPTH"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_RADI'
                'AL_DEPTH" Unit="mm" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_RADIAL_DEPTH"]}'
                '"/>\n'
                '                </Technology>\n'
                '            </ToolCutData>\n'
            )
            total_string += xml_part_str

        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_tool_cut_data generated...'
        )
        return total_string

    def set_xml_bom_components(self) -> str:
        """Set xml bom components."""
        xml_part_str = (
            '            <BOM>\n'
            '                <BOMComponent Comments=" " Na'
            'me="holder" Quantity="1" Type="HOLDER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="adapter" Quantity="1" Type="ADAPTER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="insert" Quantity="1" Type="INSERT"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="common" Quantity="1" Type="GENERAL"/>\n'
            '            </BOM>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str

    def set_xml_tail(self) -> str:
        """Set xml tail."""
        xml_part_str = (
            '            <ToolSetUpOnWorkcell>\n'
            '                <OffsetDataCollection>\n'
            '                    <OffsetData Comment="comm'
            'ent" OffsetZ="0.000000" Register="-1" Tip="1"'
            '/>\n'
            '                </OffsetDataCollection>\n'
            '            </ToolSetUpOnWorkcell>\n'
            '        </Tool>\n'
            '    </ToolingSetup>\n'
            '</MfgSetupDocument>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]} - xml_tail generated...'
        )
        return xml_part_str

    def d_for_bom(self) -> str:
        """Return the rounded diameter suffix for assembly components."""
        diam_float = float(self.tool_data['CUTTER_DIAM'])

        if 0 <= diam_float <= 20:
            diam_rounded = ceil(diam_float / 0.1) * 0.1
        elif 20 < diam_float <= 30:
            diam_rounded = ceil(diam_float / 0.5) * 0.5
        elif 30 < diam_float <= 50:
            diam_rounded = ceil(diam_float / 1) * 1
        elif 50 < diam_float <= 100:
            diam_rounded = ceil(diam_float / 5) * 5
        elif 100 < diam_float <= 200:
            diam_rounded = ceil(diam_float / 10) * 10
        elif 200 < diam_float <= 600:
            diam_rounded = ceil(diam_float / 20) * 20

        diam_rounded = round(diam_rounded, 2)

        diam_formatted = str(diam_rounded)

        if '.' in diam_formatted:
            diam_formatted = diam_formatted.replace('.', '-')
        else:
            diam_formatted = diam_formatted + '-00'

        if len(diam_formatted.split('-')[1]) == 1:
            diam_formatted += '0'
        elif len(diam_formatted.split('-')[1]) > 2:
            diam_formatted = diam_formatted[0:6:1]

        return '_D' + diam_formatted
