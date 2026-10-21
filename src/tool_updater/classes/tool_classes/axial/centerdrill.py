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


class CenterDrill(BaseTool):
    """Describe center-drill geometry and cutting data."""

    tool_material_manual = 'HSS'
    tool_type = 'CENTER-DRILLING'
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
        'iso_P': 1,
        'iso_M': 1,
        'iso_K': 1,
        'iso_N': 1,
        'iso_S': 1,
        'iso_H': 1,
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
        self.tool_size_from_geom_catalogue = tool_size_from_geom_catalogue
        self.catalog_tool_cut_data = catalog_tool_cut_data
        self.catalog_tool_geometry = catalog_tool_geometry
        self.teeth_num = teeth_num
        self.file_name_prefix = file_name_prefix
        self.file_name_suffix = file_name_suffix
        self.debug_mode = debug_mode
        super().__init__(
            tool_size_from_geom_catalogue=self.tool_size_from_geom_catalogue,
            catalog_tool_cut_data=self.catalog_tool_cut_data,
            catalog_tool_geometry=self.catalog_tool_geometry,
            teeth_num=self.teeth_num,
            file_name_prefix=self.file_name_prefix,
            file_name_suffix=self.file_name_suffix,
            debug_mode=self.debug_mode,
        )
        self.point_angle = self.get_tool_point_angle()
        # self.point_diameter = self.get_tool_point_diameter()
        self.drill_diameter = self.get_tool_drill_diameter()
        self.csink_angle = self.get_tool_csink_angle()
        self.drill_length = self.get_tool_drill_length()
        self.set_tool_xml()

    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA
    def create_tool_name_for_geom_catalogue(self) -> str:
        """Create tool name for geom catalogue."""
        t_name = self.tool_data['tool_name_str']
        return t_name

    def create_tool_name_for_cut_catalogue(self) -> float | str:
        """Create tool name for cut catalogue."""
        t_name = self.tool_data['tool_diam_float']
        return t_name

    def create_file_name(self) -> str:
        """Create file name."""
        t_prefix = self.tool_data['file_name_prefix']
        t_suffix = self.tool_data['file_name_suffix']

        d1 = self.clear_str_from_trailing_zeros(
            str(self.get_tool_drill_diameter()), sep='.'
        )
        d2 = self.clear_str_from_trailing_zeros(
            str(self.get_tool_cutter_diam()), sep='.'
        )
        l1 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['FLUTE_LENGTH']), sep='.'
        )
        l2 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['LENGTH']), sep='.'
        )

        t_name = f'{t_prefix}D{d1}_D{d2}_L{l1}_L{l2}{t_suffix}'
        return t_name

    def create_tool_name_for_xml(self) -> str:
        """Create tool name for xml."""
        t_prefix = self.tool_data['file_name_prefix'].upper()
        _t_suffix = self.tool_data['file_name_suffix'].upper()

        d1 = self.clear_str_from_trailing_zeros(
            str(self.get_tool_drill_diameter()), sep='.'
        ).replace('.', '-')
        d2 = self.clear_str_from_trailing_zeros(
            str(self.get_tool_cutter_diam()), sep='.'
        ).replace('.', '-')
        l1 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['FLUTE_LENGTH']), sep='.'
        ).replace('.', '-')
        l2 = self.clear_str_from_trailing_zeros(
            str(self.tool_data['LENGTH']), sep='.'
        ).replace('.', '-')

        t_name = (
            f'{t_prefix}D{d1}_D{d2}_L{l1}_L{l2}'
            # f"{t_suffix}"
        )
        return t_name

    def get_tool_point_angle(self) -> int:
        """Return tool point angle."""
        return cast(
            int,
            self.catalog_tool_geometry[
                self.create_tool_name_for_geom_catalogue()
            ]['point_angle'],
        )

    def get_tool_csink_angle(self) -> float:
        """Return tool csink angle."""
        return cast(
            float,
            self.catalog_tool_geometry[
                self.create_tool_name_for_geom_catalogue()
            ]['csink_angle'],
        )

    # def get_tool_point_diameter(self) -> int:
    # return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogu
    # e()]["point_diameter"]

    def get_tool_drill_diameter(self) -> float:
        """Return tool drill diameter."""
        return cast(
            float,
            self.catalog_tool_geometry[
                self.create_tool_name_for_geom_catalogue()
            ]['drill_diameter'],
        )

    def get_tool_drill_length(self) -> float:
        """Return tool drill length."""
        return cast(
            float,
            self.catalog_tool_geometry[
                self.create_tool_name_for_geom_catalogue()
            ]['drill_length'],
        )

    def get_tool_cutter_diam(self) -> float:
        """Return tool cutter diam."""
        return cast(
            float,
            self.catalog_tool_geometry[
                self.create_tool_name_for_geom_catalogue()
            ]['cutter_diam'],
        )

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
            else:
                new_str += sep + '0'

        except IndexError:
            pass
        return new_str

    def calc_len_out_of_holder(self) -> float:
        """Calculate len out of holder."""
        out_of_er = self.get_full_tool_length() - 27.5
        flute = self.get_tool_flute_length()
        diam = float(self.get_tool_cutter_diam())
        if out_of_er >= flute:
            return out_of_er
        else:
            return flute + diam

        # return self.catalog_tool_geometry[self.create_tool_name_for_geom_cata
        # logue()]["full_body_len"] / 2

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

    def calc_feed_per_unit(
        self, key_iso_material: str, fin_or_rough: str
    ) -> float:
        """Calculate feed per unit."""
        feed_multiplier = self.finishing_roughing_options[fin_or_rough][
            'feed_rate_multiplier'
        ]
        Fn = self.catalog_cut_data[key_iso_material][config.key_fn][
            self.tool_data['cut_data_diam_group']
        ]
        # RPM = self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOO
        # L_SPINDLE_RPM"]
        Fn = Fn * feed_multiplier
        return cast(float, round(Fn, ndigits=config.NDIGITS_FEED_PER_UNIT))

    def calc_radial_depth(self, key_iso_material: str) -> float:
        """Calculate radial depth."""
        return 0

    # def calc_rpm(self, Vc: int | float) -> float:
    #     try:
    #         rpm = 1000 * Vc / (pi * self.get_cutter_diam())
    #         return round(rpm, ndigits=config.NDIGITS_SPINDLE)
    #     except:
    # logger.critical(f"{self.tool_data["tool_name_str"]} - RPM not
    # calculated")
    #         return 0

    # def get_cutter_diam(self):
    # return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogu
    # e()]["cutter_diam"]

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
            '            <ModelInfo FamilyName="CENTER_DRI'
            'LL_ASM" InstanceName="CENTER_DRILL_ASM'
            f'{self.d_for_bom()}'
            '" Type="Assembly"/>\n'
            '            \n'
            '            <MfgParam Name="DRILL_DIAMETER" V'
            'alue="'
            f'{self.drill_diameter}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_DIAM" Valu'
            'e="'
            f'{self.get_tool_cutter_diam()}'
            '"/>\n'
            '            <MfgParam Name="POINT_ANGLE" Valu'
            'e="'
            f'{self.point_angle}'
            '"/>\n'
            '            <MfgParam Name="CSINK_ANGLE" Valu'
            'e="'
            f'{self.csink_angle}'
            '"/>\n'
            '            <MfgParam Name="DRILL_LENGTH" Val'
            'ue="'
            f'{self.drill_length}'
            '"/>\n'
            '            <MfgParam Name="FLUTE_LENGTH" Val'
            'ue="'
            f'{self.tool_data["FLUTE_LENGTH"]}'
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
            '"/>      \n'
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
            '                  \n'
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
            f'{self.tool_size_from_geom_catalogue}'
            ' - xml_tool_params generated...'
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
                '_PER_UNIT" Unit="mm_per_rev" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_PER_UNIT"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_AXIA'
                'L_DEPTH" Unit="mm" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_AXIAL_DEPTH"]}'
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
                '_PER_UNIT" Unit="mm_per_rev" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_PER_UNIT"]}'
                '"/>\n'
                '                    <MfgParam Name="TOOL_AXIA'
                'L_DEPTH" Unit="mm" Value="'
                f'{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_AXIAL_DEPTH"]}'
                '"/>\n'
                '                </Technology>\n'
                '            </ToolCutData>\n'
                '        '
            )
            total_string += xml_part_str

        logger.debug(
            f'{self.tool_size_from_geom_catalogue}'
            ' - xml_tool_cut_data generated...'
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
            'me="CENTER_DRILL_TAIL'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="CENTER_DRILL_CUTTER'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '            </BOM>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class CenterDrillTurnMill(CenterDrill):
    """Describe tool and holder parameters."""

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_CENTER_ASM'
    instance_name = 'TM_X_CENTER_ASM'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
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
            '        <ToolingSetup>\n'
            '            <Tool Id="'
            f'{self.tool_data["tool_name_for_xml"]}'
            '" RefXmlId="encref_1" Type="'
            f'{self.tool_data["tool_type"]}'
            '">\n'
            '                <Attr DataType="boolean" Name'
            '="UseOutline" Value="false"/>\n'
            '                <Attr DataType="boolean" Name'
            '="ProLibraryTool" Value="false"/>\n'
            '                <Attr DataType="boolean" Name'
            '="SketchTool" Value="false"/>\n'
            '                <Attr DataType="boolean" Name'
            '="ToolByRef" Value="false"/>\n'
            '\n'
            '                <ModelInfo FamilyName="'
            f'{self.family_name}'
            '" InstanceName="'
            f'{self.instance_name}'
            f'{self.d_for_bom()}'
            '" Type="Assembly"/>\n'
            '\n'
            '                <MfgParam Name="DRILL_DIAMETE'
            'R" Value="'
            f'{self.drill_diameter}'
            '"/>\n'
            '                <MfgParam Name="CUTTER_DIAM" '
            'Value="'
            f'{self.get_tool_cutter_diam()}'
            '"/>\n'
            '                <MfgParam Name="POINT_ANGLE" '
            'Value="'
            f'{self.point_angle}'
            '"/>\n'
            '                <MfgParam Name="CSINK_ANGLE" '
            'Value="'
            f'{self.csink_angle}'
            '"/>\n'
            '                <MfgParam Name="DRILL_LENGTH"'
            ' Value="'
            f'{self.drill_length}'
            '"/>\n'
            '                <MfgParam Name="FLUTE_LENGTH"'
            ' Value="'
            f'{self.tool_data["FLUTE_LENGTH"]}'
            '"/>\n'
            '                <MfgParam Name="LENGTH" Value'
            '="'
            f'{self.tool_data["len_out_of_holder"]}'
            '"/>\n'
            '\n'
            '                <MfgParam Name="SCP_TO_TAP_LE'
            'N" Value="'
            f'{self.length_taken_by_holder}'
            '"/>\n'
            '                <MfgParam Name="SAFE_LENGTH" '
            'Value="'
            f'{self.max_safe_length}'
            '"/>\n'
            '\n'
            '                <MfgParam Name="HOLDER_DIA" V'
            'alue="'
            f'{self.tool_data["HOLDER_DIA"]}'
            '"/>\n'
            '                <MfgParam Name="HOLDER_LEN" V'
            'alue="'
            f'{self.tool_data["HOLDER_LEN"]}'
            '"/>\n'
            '\n'
            '                <MfgParam Name="TOOL_COMMENT"'
            ' Value="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '                <MfgParam Name="TOOL_MATERIAL'
            '" Value="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
            '"/>\n'
            '                <MfgParam Name="LENGTH_UNITS"'
            ' Value="'
            f'{self.tool_data["LENGTH_UNITS"]}'
            '"/>\n'
            '\n'
            '                <MfgParam Name="GAUGE_X_LENGT'
            'H" Value="'
            f'{self.tool_data["GAUGE_X_LENGTH"]}'
            '"/>\n'
            '                <MfgParam Name="GAUGE_Z_LENGT'
            'H" Value="'
            f'{self.tool_data["GAUGE_Z_LENGTH"]}'
            '"/>\n'
            '                <MfgParam Name="COMP_OVERSIZE'
            '" Value="'
            f'{self.tool_data["COMP_OVERSIZE"]}'
            '"/>\n'
            '                <MfgParam Name="TOOL_LONG_FLA'
            'G" Value="'
            f'{self.tool_data["TOOL_LONG_FLAG"]}'
            '"/>\n'
            '                <MfgParam Name="COOLANT_OPTIO'
            'N" Value="'
            f'{self.tool_data["COOLANT_OPTION"]}'
            '"/>\n'
            '                <MfgParam Name="COOLANT_PRESS'
            'URE" Value="'
            f'{self.tool_data["COOLANT_PRESSURE"]}'
            '"/>\n'
            '                <MfgParam Name="SPINDLE_SENSE'
            '" Value="'
            f'{self.tool_data["SPINDLE_SENSE"]}'
            '"/>\n'
            '        '
        )
        logger.debug(
            f'{self.tool_size_from_geom_catalogue}'
            ' - xml_tool_params generated...'
        )
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


class CenterDrillTurnMill_TM_X(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_
    AXIAL_KOROTKY_EWS_107605
    """

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_CENTER'
    instance_name = 'TM_X_CENTER'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'CENTER_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'CENTER_CUT'


class CenterDrillTurnMill_TM_X_L(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_L_
    AXIAL_EWS_234762
    """

    holder_prefix = 'TM_X_L_'
    family_name = 'TM_X_L_CENTER'
    instance_name = 'TM_X_L_CENTER'
    holder_name = 'AXIAL_EWS_234762'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class CenterDrillTurnMill_TM_Z_1(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_1_
    RADIAL_1_EWS_195136
    """

    holder_prefix = 'TM_Z_1_'
    family_name = 'TM_Z_1_CENTER'
    instance_name = 'TM_Z_1_CENTER'
    holder_name = 'RADIAL_1_EWS_195136'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class CenterDrillTurnMill_TM_Z_2(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_2_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_2_'
    family_name = 'TM_Z_2_CENTER'
    instance_name = 'TM_Z_2_CENTER'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class CenterDrillTurnMill_TM_Z_SUB(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_SUB_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_SUB_'
    family_name = 'TM_Z_SUB_CENTER'
    instance_name = 'TM_Z_SUB_CENTER'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class CenterDrillTurnMill_T_Z_ER(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_ER_'
    family_name = 'T_Z_ER_CENTER'
    instance_name = 'T_Z_ER_CENTER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CENTER_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'CENTER_CUT'

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


class CenterDrillTurnMill_T_Z_SUB_ER(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_SUB_ER_'
    family_name = 'T_Z_SUB_ER_CENTER'
    instance_name = 'T_Z_SUB_ER_CENTER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CENTER_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'CENTER_CUT'

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


class CenterDrillTurnMill_T_Z(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_'
    family_name = 'T_Z_CENTER'
    instance_name = 'T_Z_CENTER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class CenterDrillTurnMill_T_Z_SUB(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_SUB_'
    family_name = 'T_Z_SUB_CENTER'
    instance_name = 'T_Z_SUB_CENTER'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class CenterDrillTurnMill_T_Z_F2(CenterDrillTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_F2_
    HOLDER_AXIS_EWS_135834
    """

    holder_prefix = 'T_Z_F2_'
    family_name = 'T_Z_F2_CENTER'
    instance_name = 'T_Z_F2_CENTER'
    holder_name = 'HOLDER_AXIS_EWS_135834'
    tail_name = 'CENTER_TAIL'
    cutter_name = 'CENTER_CUT'
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
