import logging
from math import ceil
from typing import cast

from src.tool_updater import config
from src.tool_updater.classes.tool_classes.base_tool import BaseTool
from src.tool_updater.classes.turnmill_len_adaptors import (
    adapt_flute_length,
    adapt_length,
)
from src.tool_updater.config import turnmill_holders_safe_lengths
from src.tool_updater.data_types import Catalog


logger = logging.getLogger(__name__)


class ChamferMill(BaseTool):
    """Describe tool and holder parameters."""

    tool_material_manual = 'VHM'
    # tool_type = "TAPER MILL"
    tool_type = 'MILLING'

    finishing_roughing_options = {
        'roughing': {
            'vc_modifier': 1,  # Множитель для подачи (и на зуб, и на оборот)
            'feed_rate_multiplier': 0.6,  # Множитель для скорости резания
        },
        'finishing': {
            'vc_modifier': 1,
            'feed_rate_multiplier': 0.6,
        },
    }

    axial_depth_modifiyers = {
        'iso_P': 0.3,
        'iso_M': 0.3,
        'iso_K': 0.3,
        'iso_N': 0.3,
        'iso_S': 0.3,
        'iso_H': 0.3,
    }
    radial_depth_modifiyers = {
        'iso_P': 0.15,
        'iso_M': 0.1,
        'iso_K': 0.1,
        'iso_N': 0.2,
        'iso_S': 0.1,
        'iso_H': 0.025,
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
        self.complex_size_name = tool_size_from_geom_catalogue

        self.catalog_tool_cut_data = catalog_tool_cut_data
        self.catalog_tool_geometry = catalog_tool_geometry
        self.teeth_num = teeth_num
        self.file_name_prefix = file_name_prefix
        self.file_name_suffix = file_name_suffix
        self.debug_mode = debug_mode
        super().__init__(
            tool_size_from_geom_catalogue=self.complex_size_name,
            # tool_size_from_geom_catalogue=self.tool_size_from_geom_catalogue,
            catalog_tool_cut_data=self.catalog_tool_cut_data,
            catalog_tool_geometry=self.catalog_tool_geometry,
            teeth_num=self.teeth_num,
            file_name_prefix=self.file_name_prefix,
            file_name_suffix=self.file_name_suffix,
            debug_mode=self.debug_mode,
        )
        self.corner_radius = self.get_corner_radius()
        self.side_angle = self.get_side_angle()
        self.shank_diam = self.get_shank_diam()
        self.tip_diam = self.get_tip_diam()

    def get_shank_diam(self) -> float:
        """Return shank diam."""
        return cast(
            float,
            self.catalog_tool_geometry[self.complex_size_name]['flute_diam'],
        )

    def get_tip_diam(self) -> float:
        """Return tip diam."""
        try:
            return cast(
                float,
                self.catalog_tool_geometry[self.complex_size_name]['tip_diam'],
            )
        except KeyError:
            return 0.2

    def get_corner_radius(self) -> float:
        """Return corner radius."""
        return 0

    def get_side_angle(self) -> float:
        """Return side angle."""
        return cast(
            float,
            self.catalog_tool_geometry[self.complex_size_name]['side_angle'],
        )

    def calc_len_out_of_holder(self) -> float:
        """Calculate len out of holder."""
        hol_len = self.catalog_tool_geometry[self.complex_size_name][
            'full_body_len'
        ]
        _flute_len = self.catalog_tool_geometry[self.complex_size_name][
            'flute_len'
        ]
        return cast(float, hol_len - 25)

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
        angle = self.clear_str_from_trailing_zeros(
            str(self.get_side_angle() * 2), sep='.'
        ).replace('.', '-')
        l1 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['FLUTE_LENGTH']), sep='.'
        ).replace('.', '-')
        l2 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['LENGTH']), sep='.'
        ).replace('.', '-')

        t_name = (
            f'{t_prefix}D{d}x{angle}_L{l1}-L{l2}'
            # f"{t_suffix}"
        )
        return t_name

    def create_file_name(self) -> str:
        """Create file name."""
        t_prefix = self.tool_data['file_name_prefix']
        t_suffix = self.tool_data['file_name_suffix']

        d = self.clear_str_from_trailing_zeros(
            str(self.tool_data['CUTTER_DIAM']), sep='.'
        )
        angle = self.get_side_angle() * 2
        l1 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['FLUTE_LENGTH']), sep='.'
        )
        l2 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['LENGTH']), sep='.'
        )

        t_name = f'{t_prefix}D{d}x{angle}_L{l1}-L{l2}{t_suffix}'
        return t_name

    def calc_feed_rate(
        self, key_iso_material: str, RPM: float, fin_or_rough: str
    ) -> float:
        """Calculate feed rate."""
        feed_multiplier = self.finishing_roughing_options[fin_or_rough][
            'feed_rate_multiplier'
        ]
        F = self.catalog_cut_data[key_iso_material][config.key_f][
            self.tool_data['cut_data_diam_group']
        ]
        F *= feed_multiplier
        return cast(float, round(F, ndigits=config.NDIGITS_FEED))

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
            '            \n'
            '            <ModelInfo FamilyName="CHAMFER_MI'
            'LL_ASM" InstanceName="CHAMFER_MILL_ASM'
            f'{self.d_for_bom()}'
            '" Type="Assembly"/>\n'
            '            \n'
            '            <MfgParam Name="CUTTER_DIAM" Valu'
            'e="'
            f'{self.tip_diam}'
            '"/>\n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.shank_diam}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.corner_radius}'
            '"/>\n'
            '            <MfgParam Name="CUT_LENGTH" Value'
            '="'
            f'{self.tool_data["FLUTE_LENGTH"]}'
            '"/>\n'
            '            <MfgParam Name="SIDE_ANGLE" Value'
            '="'
            f'{self.side_angle}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="LENGTH" Value="'
            f'{self.tool_data["len_out_of_holder"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="HOLDER_DIA" Value'
            '="'
            f'{self.tool_data["HOLDER_DIA"]}'
            '"/>\n'
            '            <MfgParam Name="HOLDER_LEN" Value'
            '="'
            f'{self.tool_data["HOLDER_LEN"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
            '"/>\n'
            '            <MfgParam Name="LENGTH_UNITS" Val'
            'ue="'
            f'{self.tool_data["LENGTH_UNITS"]}'
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
            '    '
        )
        logger.debug(
            f'{self.complex_size_name} - xml_tool_params generated...'
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
                '        '
            )
            total_string += xml_part_str

        logger.debug(
            f'{self.complex_size_name} - xml_tool_cut_data generated...'
        )
        return total_string

    def set_xml_bom_components(self) -> str:
        """Set xml bom components."""
        xml_part_str = (
            '            <BOM>\n'
            '                <BOMComponent Comments=" " Na'
            'me="BT40_COLLET_CHUCK" Quantity="1" Type="HOL'
            'DER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="BT40-45_PULL_STUD" Quantity="1" Type="HOL'
            'DER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="BT40_HOLDER'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="CHAMFER_MILL_TAIL'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="CHAMFER_MILL_CUTTER'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '            </BOM>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class ChamferTurnMill(ChamferMill):
    """Describe tool and holder parameters."""

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_CHAMFER_ASM'
    instance_name = 'TM_X_CHAMFER_ASM'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

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

        diam_rounded = round(diam_rounded, 1)

        # diam_rounded = ceil(diam_float * 10) / 10
        diam_formatted = str(diam_rounded)

        # diam_formatted = (str(self.tool_data["CUTTER_DIAM"]))

        if '.' in diam_formatted:
            diam_formatted = diam_formatted.replace('.', '-')
        else:
            diam_formatted = diam_formatted + '-0'

        if len(diam_formatted.split('-')[1]) == 1:
            # diam_formatted += "0"
            pass
        elif len(diam_formatted.split('-')[1]) > 1:
            diam_formatted = diam_formatted[0:5:1]

        return '_D' + diam_formatted

    def adapt_drill_lengths(self) -> None:
        """Adapt drill lengths."""
        self.tool_data['len_out_of_holder'] = adapt_length(
            max_safe_length=self.max_safe_length,
            length_taken_by_holder=self.length_taken_by_holder,
            default_full_length=self.tool_data['len_out_of_holder'],
        )
        self.tool_data['FLUTE_LENGTH'] = adapt_flute_length(
            default_flute_length=self.tool_data['FLUTE_LENGTH'],
            full_length_adapted=self.tool_data['len_out_of_holder'],
        )

    def set_xml_body_tool_params(self) -> str:
        """Set xml body tool params."""
        self.adapt_drill_lengths()
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
            '\n'
            '            <ModelInfo FamilyName="'
            f'{self.family_name}'
            '" InstanceName="'
            f'{self.instance_name}'
            f'{self.d_for_bom()}'
            '" Type="Assembly"/>\n'
            '\n'
            '            <MfgParam Name="CUTTER_DIAM" Valu'
            'e="'
            f'{self.tip_diam}'
            '"/>\n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.shank_diam}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.corner_radius}'
            '"/>\n'
            '            <MfgParam Name="CUT_LENGTH" Value'
            '="'
            f'{self.tool_data["FLUTE_LENGTH"]}'
            '"/>\n'
            '            <MfgParam Name="SIDE_ANGLE" Value'
            '="'
            f'{self.side_angle}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="LENGTH" Value="'
            f'{self.tool_data["len_out_of_holder"]}'
            '"/>\n'
            '\n'
            '            <MfgParam Name="HOLDER_DIA" Value'
            '="'
            f'{self.tool_data["HOLDER_DIA"]}'
            '"/>\n'
            '            <MfgParam Name="HOLDER_LEN" Value'
            '="'
            f'{self.tool_data["HOLDER_LEN"]}'
            '"/>\n'
            '\n'
            '            <MfgParam Name="SCP_TO_TAP_LEN" V'
            'alue="'
            f'{self.length_taken_by_holder}'
            '"/>\n'
            '            <MfgParam Name="SAFE_LENGTH" Valu'
            'e="'
            f'{self.max_safe_length}'
            '"/>\n'
            '\n'
            '            <MfgParam Name="LENGTH_UNITS" Val'
            'ue="'
            f'{self.tool_data["LENGTH_UNITS"]}'
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
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '        '
        )
        # logger.debug(f"{self.tool_size_from_geom_catalogue} - xml_tool_params
        # generated...")
        return xml_part_str

    def set_xml_bom_components(self) -> str:
        """Set xml bom components."""
        xml_part_str = (
            '                <BOM>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.holder_name}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.tail_name}'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.cutter_name}'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '                </BOM>\n'
            '    '
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class ChamferTurnMill_TM_X(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_
    AXIAL_KOROTKY_EWS_107605
    """

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_CHAMFER'
    instance_name = 'TM_X_CHAMFER'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'CHAMFER_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'CHAMFER_CUT'


class ChamferTurnMill_TM_X_L(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_L_
    AXIAL_EWS_234762
    """

    holder_prefix = 'TM_X_L_'
    family_name = 'TM_X_L_CHAMFER'
    instance_name = 'TM_X_L_CHAMFER'
    holder_name = 'AXIAL_EWS_234762'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class ChamferTurnMill_TM_Z_1(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_1_
    RADIAL_1_EWS_195136
    """

    holder_prefix = 'TM_Z_1_'
    family_name = 'TM_Z_1_CHAMFER'
    instance_name = 'TM_Z_1_CHAMFER'
    holder_name = 'RADIAL_1_EWS_195136'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class ChamferTurnMill_TM_Z_2(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_2_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_2_'
    family_name = 'TM_Z_2_CHAMFER'
    instance_name = 'TM_Z_2_CHAMFER'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class ChamferTurnMill_TM_Z_SUB(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_SUB_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_SUB_'
    family_name = 'TM_Z_SUB_CHAMFER'
    instance_name = 'TM_Z_SUB_CHAMFER'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class ChamferTurnMill_T_Z_ER(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_ER_'
    family_name = 'T_Z_ER_CHAMFER'
    instance_name = 'T_Z_ER_CHAMFER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CHAMFER_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'CHAMFER_CUT'

    def set_xml_bom_components(self) -> str:
        """Set xml bom components."""
        xml_part_str = (
            '                <BOM>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.holder_name}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.tail_name}'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="HOLDER_COLLETS" Quantity="2" Type="HO'
            'LDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.cutter_name}'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '                </BOM>\n'
            '    '
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class ChamferTurnMill_T_Z_SUB_ER(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_SUB_ER_'
    family_name = 'T_Z_SUB_ER_CHAMFER'
    instance_name = 'T_Z_SUB_ER_CHAMFER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CHAMFER_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'CHAMFER_CUT'

    def set_xml_bom_components(self) -> str:
        """Set xml bom components."""
        xml_part_str = (
            '                <BOM>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.holder_name}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.tail_name}'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="HOLDER_COLLETS" Quantity="2" Type="HO'
            'LDER"/>\n'
            '                    <BOMComponent Comments=" '
            '" Name="'
            f'{self.cutter_name}'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '                </BOM>\n'
            '    '
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class ChamferTurnMill_T_Z(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_'
    family_name = 'T_Z_CHAMFER'
    instance_name = 'T_Z_CHAMFER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class ChamferTurnMill_T_Z_SUB(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_SUB_'
    family_name = 'T_Z_SUB_CHAMFER'
    instance_name = 'T_Z_SUB_CHAMFER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class ChamferTurnMill_T_Z_F2(ChamferTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_F2_
    HOLDER_AXIS_EWS_135834
    """

    holder_prefix = 'T_Z_F2_'
    family_name = 'T_Z_F2_CHAMFER'
    instance_name = 'T_Z_F2_CHAMFER'
    holder_name = 'HOLDER_AXIS_EWS_135834'
    tail_name = 'CHAMFER_TAIL'
    cutter_name = 'CHAMFER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


"""
TM_X_
    AXIAL_KOROTKY_EWS_107605
TM_X_L_
    AXIAL_EWS_234762
TM_Z_1_
    RADIAL_1_EWS_195136
TM_Z_2_
    RADIAL_2_EWS_196914
TM_Z_SUB_
    RADIAL_2_EWS_196914
T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
T_Z_
    HOLDER_L85_S02361
T_Z_SUB_
    HOLDER_L85_S02361
T_Z_F2_
    HOLDER_AXIS_EWS_135834
"""

"""
TM_X_
TM_X_L_
TM_Z_1_
TM_Z_2_
TM_Z_SUB_
T_Z_ER_
T_Z_SUB_ER_
T_Z_
T_Z_SUB_
T_Z_F2_
"""
