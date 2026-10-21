import json
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


class GribMillFlat(BaseTool):
    """Describe tool and holder parameters."""

    tool_material_manual = 'Carbide inserts'
    tool_type = 'SIDE_MILLING'

    finishing_roughing_options = {
        'roughing': {
            'vc_modifier': 1,  # Множитель для подачи (и на зуб, и на оборот)
            'feed_rate_multiplier': 0.6,  # Множитель для скорости резания
        },
        'finishing': {
            'vc_modifier': 1.1,
            'feed_rate_multiplier': 0.5,
        },
    }

    key_ae = 'Ae'
    key_holder_size = 'holder_name'

    axial_depth_modifiyers = {
        'iso_P': 1,
        'iso_M': 1,
        'iso_K': 1,
        'iso_N': 1,
        'iso_S': 1,
        'iso_H': 1,
    }
    radial_depth_modifiyers = {
        'iso_P': 1,
        'iso_M': 1,
        'iso_K': 1,
        'iso_N': 1,
        'iso_S': 1,
        'iso_H': 1,
    }

    path_to_holder_geometry_catalog = (
        config.CATALOGS_DIR
        / 'milling'
        / 'gribkovie'
        / 'Iscar'
        / 'MultiMaster'
        / 'holders_for_MultiMaster.json'
    )

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

        with self.path_to_holder_geometry_catalog.open(encoding='utf-8') as f:
            self.catalog_holder_geometry = json.load(f)

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
        self.tool_data['CORNER_RADIUS'] = (
            self.get_tool_corner_radius_from_complex_size()
        )
        self.tool_data['CORNER_CHAMFER'] = (
            self.get_tool_corner_chamfer_from_complex_size()
        )
        self.tool_data['CORNER_CHAMFER_ANGLE'] = (
            self.get_tool_corner_chamfer_angle_from_complex_size()
        )
        self.tool_data['CUTTER_WIDTH'] = (
            self.get_tool_cutter_width_from_complex_size()
        )
        self.tool_data['SHANK_DIAM'] = self.get_tool_shank_diam()

    def get_tool_flute_diam_from_complex_size(self) -> str:
        """Return tool flute diam from complex size."""
        return self.complex_size_name.split(sep=' ')[0]

    def get_tool_cutter_width_from_complex_size(self) -> str:
        """Return tool cutter width from complex size."""
        w = self.complex_size_name.split(sep=' ')[1].replace('W', '')
        while len(w.split(sep='.')[1]) < 2:
            w += '0'
        return w

    def get_tool_corner_radius_from_complex_size(self) -> str:
        """Return tool corner radius from complex size."""
        return self.complex_size_name.split(sep=' ')[2].replace('R', '')

    def get_tool_corner_chamfer_from_complex_size(self) -> str:
        """Return tool corner chamfer from complex size."""
        return self.complex_size_name.split(sep=' ')[3].replace('C', '')

    def get_tool_corner_chamfer_angle_from_complex_size(self) -> str:
        """Return tool corner chamfer angle from complex size."""
        return self.complex_size_name.split(sep=' ')[4].replace('A', '')

    def get_tool_shank_diam(self) -> float:
        """Return tool shank diam."""
        hol_size = self.get_tool_holder_size()
        return cast(
            float, self.catalog_holder_geometry[hol_size]['lowering_diam']
        )

    def get_tool_diam_float(self) -> float:
        """Return tool diam float."""
        return float(self.get_tool_flute_diam_from_complex_size())

    def get_cutter_diam(self) -> str:
        """Return cutter diam."""
        return self.get_tool_flute_diam_from_complex_size()

    def calc_axial_depth(self, key_iso_material: str) -> float:
        """Calculate axial depth."""
        return float(self.get_tool_cutter_width_from_complex_size())

    def calc_radial_depth(self, key_iso_material: str) -> float:
        """Calculate radial depth."""
        return cast(
            float,
            self.catalog_tool_geometry[self.complex_size_name][
                'max_cut_depth'
            ],
        )

    # def get_holder_len(self):
    #     hol_size = self.get_tool_holder_size()
    #     l = self.catalog_holder_geometry[hol_size]["holder_len"]
    #     return l

    def get_tool_holder_size(self) -> str:
        """Return tool holder size."""
        hol_size = self.catalog_tool_geometry[self.complex_size_name][
            self.key_holder_size
        ]
        return cast(str, hol_size)

    def get_full_tool_length(self) -> float:
        """Return full tool length."""
        hol_size = self.get_tool_holder_size()
        hol_len = self.catalog_holder_geometry[hol_size]['holder_full_len']
        return cast(float, hol_len)

    def calc_len_out_of_holder(self) -> float:
        """Calculate len out of holder."""
        hol_size = self.get_tool_holder_size()
        hol_body_min_len = self.catalog_holder_geometry[hol_size][
            'len_to_lowering_start'
        ]
        return cast(float, hol_body_min_len)

    def calc_feed_per_unit(
        self, key_iso_material: str, fin_or_rough: str
    ) -> float:
        """Calculate feed per unit."""
        cut_w = self.get_tool_cutter_width_from_complex_size()
        Fz = self.catalog_cut_data[key_iso_material][config.key_fz][cut_w]
        # Fz =
        # str(self.catalog_cut_data[key_iso_material][config.key_fz][cut_w])
        # while len(Fz.split(sep=".")[1]) < 2:
        #     Fz += "0"
        return cast(float, Fz)

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
            cast(str, self.tool_data['CUTTER_DIAM']), sep='.'
        ).replace('.', '-')
        w = self.clear_str_from_trailing_zeros(
            self.get_tool_cutter_width_from_complex_size(), sep='.'
        ).replace('.', '-')
        r = self.clear_str_from_trailing_zeros(
            self.get_tool_corner_radius_from_complex_size(), sep='.'
        ).replace('.', '-')
        # r = self.get_tool_corner_radius_from_complex_size().replace(".", "-")
        c = self.clear_str_from_trailing_zeros(
            self.get_tool_corner_chamfer_from_complex_size(), sep='.'
        ).replace('.', '-')
        a = self.clear_str_from_trailing_zeros(
            self.get_tool_corner_chamfer_angle_from_complex_size(), sep='.'
        ).replace('.', '-')
        l1 = self.clear_str_from_trailing_zeros(
            str(self.calc_len_out_of_holder()), sep='.'
        ).replace('.', '-')
        l2 = self.clear_str_from_trailing_zeros(
            str(self.get_full_tool_length()), sep='.'
        ).replace('.', '-')
        if r == '0' and c == '0':
            t_name = (
                f'{t_prefix}D{d}_W{w}_L{l1}_L{l2}'
                # f"{t_suffix}"
            )
        elif r == '0' and c != '0' and a != '0':
            t_name = (
                f'{t_prefix}D{d}_W{w}_C{c}_A{a}_L{l1}_L{l2}'
                # f"{t_suffix}"
            )
        elif r != '0' and c == '0':
            t_name = (
                f'{t_prefix}D{d}_W{w}_R{r}_L{l1}_L{l2}'
                # f"{t_suffix}"
            )
        else:
            t_name = (
                f'{t_prefix}D{d}_W{w}_R{r}_C{c}_A{a}_L{l1}_L{l2}'
                # f"{t_suffix}"
            )

        return t_name

    def create_file_name(self) -> str:
        """Create file name."""
        t_prefix = self.tool_data['file_name_prefix']
        t_suffix = self.tool_data['file_name_suffix']

        d = self.clear_str_from_trailing_zeros(
            cast(str, self.tool_data['CUTTER_DIAM']), sep='.'
        )
        w = self.clear_str_from_trailing_zeros(
            self.get_tool_cutter_width_from_complex_size(), sep='.'
        )
        # r = self.clear_str_from_trailing_zeros(self.get_tool_corner_radius_fr
        # om_complex_size(), sep=".")
        r = self.get_tool_corner_radius_from_complex_size()
        c = self.clear_str_from_trailing_zeros(
            self.get_tool_corner_chamfer_from_complex_size(), sep='.'
        )
        a = self.clear_str_from_trailing_zeros(
            self.get_tool_corner_chamfer_angle_from_complex_size(), sep='.'
        )
        l1 = self.clear_str_from_trailing_zeros(
            str(self.calc_len_out_of_holder()), sep='.'
        )
        l2 = self.clear_str_from_trailing_zeros(
            str(self.get_full_tool_length()), sep='.'
        )

        if r == '0' and c == '0':
            t_name = f'{t_prefix}D{d}_W{w}_L{l1}_L{l2}{t_suffix}'
        elif r == '0' and c != '0' and a != '0':
            t_name = f'{t_prefix}D{d}_W{w}_C{c}_A{a}_L{l1}_L{l2}{t_suffix}'
        elif r != '0' and c == '0':
            t_name = f'{t_prefix}D{d}_W{w}_R{r}_L{l1}_L{l2}{t_suffix}'
        else:
            t_name = (
                f'{t_prefix}D{d}_W{w}_R{r}_C{c}_A{a}_L{l1}_L{l2}{t_suffix}'
            )
        return t_name

    def calc_feed_rate(
        self, key_iso_material: str, RPM: float, fin_or_rough: str
    ) -> float:
        """Calculate feed rate."""
        feed_multiplier = self.finishing_roughing_options[fin_or_rough][
            'feed_rate_multiplier'
        ]
        Fz = self.catalog_cut_data[key_iso_material][config.key_fz][
            self.get_tool_cutter_width_from_complex_size()
        ]
        z = self.catalog_tool_geometry[self.complex_size_name][
            config.key_num_of_teeth
        ]
        F = Fz * z * RPM * feed_multiplier
        return cast(float, round(F, ndigits=config.NDIGITS_FEED))

    def get_tool_teeth_num(self) -> int:
        """Return tool teeth num."""
        return cast(
            int,
            self.catalog_tool_geometry[self.complex_size_name][
                config.key_num_of_teeth
            ],
        )

    # def calc_nut_diam(self) -> int:
    #     return self.get_tool_shank_diam() + 20

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
            '            <ModelInfo FamilyName="SIDE_MILL_'
            'FLAT_ASM" InstanceName="SIDE_MILL_FLAT_ASM'
            f'{self.d_for_bom()}'
            '" Type="Assembly"/>\n'
            '\n'
            '            <MfgParam Name="CUTTER_DIAM" Valu'
            'e="'
            f'{self.tool_data["CUTTER_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.tool_data["CORNER_RADIUS"]}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_WIDTH" Val'
            'ue="'
            f'{self.tool_data["CUTTER_WIDTH"]}'
            '"/>\n'
            '\n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.tool_data["SHANK_DIAM"]}'
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
            ' \n'
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
            '"/>\n'
            '            \n'
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
            'me="SIDE_MILL_FLAT_TAIL'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="SIDE_MILL_FLAT_CUTTER'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '            </BOM>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class GribMillChamfer(GribMillFlat):
    """Describe tool and holder parameters."""

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
            '            <ModelInfo FamilyName="SIDE_MILL_'
            'CHAMF_ASM" InstanceName="SIDE_MILL_CHAMF_ASM'
            f'{self.d_for_bom()}'
            '" Type="Assembly"/>\n'
            '            \n'
            '            <MfgParam Name="CUTTER_DIAM" Valu'
            'e="'
            f'{self.tool_data["CUTTER_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.tool_data["CORNER_CHAMFER"]}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_WIDTH" Val'
            'ue="'
            f'{self.tool_data["CUTTER_WIDTH"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.tool_data["SHANK_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="LENGTH" Value="'
            f'{self.tool_data["len_out_of_holder"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="CORNER_CHAMFER" V'
            'alue="'
            f'{self.tool_data["CORNER_CHAMFER"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_CHAMFER_AN'
            'GLE" Value="'
            f'{self.tool_data["CORNER_CHAMFER_ANGLE"]}'
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
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
            '"/>\n'
            '            \n'
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
            'me="SIDE_MILL_CHAMF_TAIL'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="SIDE_MILL_CHAMF_CUTTER'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '            </BOM>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class GribMillRounding(GribMillFlat):
    """Describe tool and holder parameters."""

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
            '            <ModelInfo FamilyName="SIDE_MILL_'
            'ROUND_ASM" InstanceName="SIDE_MILL_ROUND_ASM'
            f'{self.d_for_bom()}'
            '" Type="Assembly"/>\n'
            '            \n'
            '            <MfgParam Name="CUTTER_DIAM" Valu'
            'e="'
            f'{self.tool_data["CUTTER_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.tool_data["CORNER_RADIUS"]}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_WIDTH" Val'
            'ue="'
            f'{self.tool_data["CUTTER_WIDTH"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="CORNER_CHAMFER" V'
            'alue="'
            f'{self.tool_data["CORNER_CHAMFER"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_CHAMFER_AN'
            'GLE" Value="'
            f'{self.tool_data["CORNER_CHAMFER_ANGLE"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.tool_data["SHANK_DIAM"]}'
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
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
            '"/>\n'
            '            \n'
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
            'me="SIDE_MILL_ROUND_TAIL'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="HOLDER"/>\n'
            '                <BOMComponent Comments=" " Na'
            'me="SIDE_MILL_ROUND_CUTTER'
            f'{self.d_for_bom()}'
            '" Quantity="1" Type="GENERAL"/>\n'
            '            </BOM>\n'
        )
        logger.debug(
            f'{self.tool_data["tool_name_str"]}'
            ' - xml_BOM_components generated...'
        )
        return xml_part_str


class Grib_FlTurnMill(GribMillFlat):
    """Describe tool and holder parameters."""

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_SIDE_FL_ASM'
    instance_name = 'TM_X_SIDE_FL_ASM'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
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
            f'{self.tool_data["CUTTER_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.tool_data["CORNER_RADIUS"]}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_WIDTH" Val'
            'ue="'
            f'{self.tool_data["CUTTER_WIDTH"]}'
            '"/>\n'
            '\n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.tool_data["SHANK_DIAM"]}'
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
            ' \n'
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
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


class Grib_FlTurnMill_TM_X(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_
    AXIAL_KOROTKY_EWS_107605
    """

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_SIDE_FL'
    instance_name = 'TM_X_SIDE_FL'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'SIDE_FL_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_FL_CUT'


class Grib_FlTurnMill_TM_X_L(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_L_
    AXIAL_EWS_234762
    """

    holder_prefix = 'TM_X_L_'
    family_name = 'TM_X_L_SIDE_FL'
    instance_name = 'TM_X_L_SIDE_FL'
    holder_name = 'AXIAL_EWS_234762'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_FlTurnMill_TM_Z_1(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_1_
    RADIAL_1_EWS_195136
    """

    holder_prefix = 'TM_Z_1_'
    family_name = 'TM_Z_1_SIDE_FL'
    instance_name = 'TM_Z_1_SIDE_FL'
    holder_name = 'RADIAL_1_EWS_195136'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_FlTurnMill_TM_Z_2(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_2_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_2_'
    family_name = 'TM_Z_2_SIDE_FL'
    instance_name = 'TM_Z_2_SIDE_FL'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_FlTurnMill_TM_Z_SUB(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_SUB_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_SUB_'
    family_name = 'TM_Z_SUB_SIDE_FL'
    instance_name = 'TM_Z_SUB_SIDE_FL'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_FlTurnMill_T_Z_ER(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_ER_'
    family_name = 'T_Z_ER_SIDE_FL'
    instance_name = 'T_Z_ER_SIDE_FL'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_FL_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_FL_CUT'

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


class Grib_FlTurnMill_T_Z_SUB_ER(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_SUB_ER_'
    family_name = 'T_Z_SUB_ER_SIDE_FL'
    instance_name = 'T_Z_SUB_ER_SIDE_FL'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_FL_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_FL_CUT'

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


class Grib_FlTurnMill_T_Z(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_'
    family_name = 'T_Z_SIDE_FL'
    instance_name = 'T_Z_SIDE_FL'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_FlTurnMill_T_Z_SUB(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_SUB_'
    family_name = 'T_Z_SUB_SIDE_FL'
    instance_name = 'T_Z_SUB_SIDE_FL'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_FlTurnMill_T_Z_F2(Grib_FlTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_F2_
    HOLDER_AXIS_EWS_135834
    """

    holder_prefix = 'T_Z_F2_'
    family_name = 'T_Z_F2_SIDE_FL'
    instance_name = 'T_Z_F2_SIDE_FL'
    holder_name = 'HOLDER_AXIS_EWS_135834'
    tail_name = 'SIDE_FL_TAIL'
    cutter_name = 'SIDE_FL_CUT'
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


class Grib_ChTurnMill(GribMillChamfer):
    """Describe tool and holder parameters."""

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_SIDE_CH_ASM'
    instance_name = 'TM_X_SIDE_CH_ASM'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
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
            f'{self.tool_data["CUTTER_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.tool_data["CORNER_CHAMFER"]}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_WIDTH" Val'
            'ue="'
            f'{self.tool_data["CUTTER_WIDTH"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.tool_data["SHANK_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="LENGTH" Value="'
            f'{self.tool_data["len_out_of_holder"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="CORNER_CHAMFER" V'
            'alue="'
            f'{self.tool_data["CORNER_CHAMFER"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_CHAMFER_AN'
            'GLE" Value="'
            f'{self.tool_data["CORNER_CHAMFER_ANGLE"]}'
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
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
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


class Grib_ChTurnMill_TM_X(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_
    AXIAL_KOROTKY_EWS_107605
    """

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_SIDE_CH'
    instance_name = 'TM_X_SIDE_CH'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'SIDE_CH_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_CH_CUT'


class Grib_ChTurnMill_TM_X_L(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_L_
    AXIAL_EWS_234762
    """

    holder_prefix = 'TM_X_L_'
    family_name = 'TM_X_L_SIDE_CH'
    instance_name = 'TM_X_L_SIDE_CH'
    holder_name = 'AXIAL_EWS_234762'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_ChTurnMill_TM_Z_1(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_1_
    RADIAL_1_EWS_195136
    """

    holder_prefix = 'TM_Z_1_'
    family_name = 'TM_Z_1_SIDE_CH'
    instance_name = 'TM_Z_1_SIDE_CH'
    holder_name = 'RADIAL_1_EWS_195136'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_ChTurnMill_TM_Z_2(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_2_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_2_'
    family_name = 'TM_Z_2_SIDE_CH'
    instance_name = 'TM_Z_2_SIDE_CH'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_ChTurnMill_TM_Z_SUB(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_SUB_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_SUB_'
    family_name = 'TM_Z_SUB_SIDE_CH'
    instance_name = 'TM_Z_SUB_SIDE_CH'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_ChTurnMill_T_Z_ER(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_ER_'
    family_name = 'T_Z_ER_SIDE_CH'
    instance_name = 'T_Z_ER_SIDE_CH'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_CH_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_CH_CUT'

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


class Grib_ChTurnMill_T_Z_SUB_ER(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_SUB_ER_'
    family_name = 'T_Z_SUB_ER_SIDE_CH'
    instance_name = 'T_Z_SUB_ER_SIDE_CH'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_CH_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_CH_CUT'

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


class Grib_ChTurnMill_T_Z(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_'
    family_name = 'T_Z_SIDE_CH'
    instance_name = 'T_Z_SIDE_CH'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_ChTurnMill_T_Z_SUB(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_SUB_'
    family_name = 'T_Z_SUB_SIDE_CH'
    instance_name = 'T_Z_SUB_SIDE_CH'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_ChTurnMill_T_Z_F2(Grib_ChTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_F2_
    HOLDER_AXIS_EWS_135834
    """

    holder_prefix = 'T_Z_F2_'
    family_name = 'T_Z_F2_SIDE_CH'
    instance_name = 'T_Z_F2_SIDE_CH'
    holder_name = 'HOLDER_AXIS_EWS_135834'
    tail_name = 'SIDE_CH_TAIL'
    cutter_name = 'SIDE_CH_CUT'
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


class Grib_RoTurnMill(GribMillRounding):
    """Describe tool and holder parameters."""

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_SIDE_RO_ASM'
    instance_name = 'TM_X_SIDE_RO_ASM'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
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
            f'{self.tool_data["CUTTER_DIAM"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_RADIUS" Va'
            'lue="'
            f'{self.tool_data["CORNER_RADIUS"]}'
            '"/>\n'
            '            <MfgParam Name="CUTTER_WIDTH" Val'
            'ue="'
            f'{self.tool_data["CUTTER_WIDTH"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="CORNER_CHAMFER" V'
            'alue="'
            f'{self.tool_data["CORNER_CHAMFER"]}'
            '"/>\n'
            '            <MfgParam Name="CORNER_CHAMFER_AN'
            'GLE" Value="'
            f'{self.tool_data["CORNER_CHAMFER_ANGLE"]}'
            '"/>\n'
            '            \n'
            '            <MfgParam Name="SHANK_DIAM" Value'
            '="'
            f'{self.tool_data["SHANK_DIAM"]}'
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
            '            <MfgParam Name="NUM_OF_TEETH" Val'
            'ue="'
            f'{self.tool_data["NUM_OF_TEETH"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_COMMENT" Val'
            'ue="'
            f'{self.tool_data["TOOL_COMMENT"]}'
            '"/>\n'
            '            <MfgParam Name="TOOL_MATERIAL" Va'
            'lue="'
            f'{self.tool_data["TOOL_MATERIAL"]}'
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


class Grib_RoTurnMill_TM_X(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_
    AXIAL_KOROTKY_EWS_107605
    """

    holder_prefix = 'TM_X_'
    family_name = 'TM_X_SIDE_RO'
    instance_name = 'TM_X_SIDE_RO'
    holder_name = 'AXIAL_KOROTKY_EWS_107605'
    tail_name = 'SIDE_RO_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_RO_CUT'


class Grib_RoTurnMill_TM_X_L(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    TM_X_L_
    AXIAL_EWS_234762
    """

    holder_prefix = 'TM_X_L_'
    family_name = 'TM_X_L_SIDE_RO'
    instance_name = 'TM_X_L_SIDE_RO'
    holder_name = 'AXIAL_EWS_234762'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_RoTurnMill_TM_Z_1(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_1_
    RADIAL_1_EWS_195136
    """

    holder_prefix = 'TM_Z_1_'
    family_name = 'TM_Z_1_SIDE_RO'
    instance_name = 'TM_Z_1_SIDE_RO'
    holder_name = 'RADIAL_1_EWS_195136'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_RoTurnMill_TM_Z_2(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_2_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_2_'
    family_name = 'TM_Z_2_SIDE_RO'
    instance_name = 'TM_Z_2_SIDE_RO'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_RoTurnMill_TM_Z_SUB(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    TM_Z_SUB_
    RADIAL_2_EWS_196914
    """

    holder_prefix = 'TM_Z_SUB_'
    family_name = 'TM_Z_SUB_SIDE_RO'
    instance_name = 'TM_Z_SUB_SIDE_RO'
    holder_name = 'RADIAL_2_EWS_196914'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_RoTurnMill_T_Z_ER(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_ER_'
    family_name = 'T_Z_ER_SIDE_RO'
    instance_name = 'T_Z_ER_SIDE_RO'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_RO_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_RO_CUT'

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


class Grib_RoTurnMill_T_Z_SUB_ER(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """

    holder_prefix = 'T_Z_SUB_ER_'
    family_name = 'T_Z_SUB_ER_SIDE_RO'
    instance_name = 'T_Z_SUB_ER_SIDE_RO'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_RO_TAIL'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]

    cutter_name = 'SIDE_RO_CUT'

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


class Grib_RoTurnMill_T_Z(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_'
    family_name = 'T_Z_SIDE_RO'
    instance_name = 'T_Z_SIDE_RO'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_RoTurnMill_T_Z_SUB(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_SUB_
    HOLDER_L85_S02361
    """

    holder_prefix = 'T_Z_SUB_'
    family_name = 'T_Z_SUB_SIDE_RO'
    instance_name = 'T_Z_SUB_SIDE_RO'
    holder_name = 'HOLDER_L85_S02361'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix][
        'max_safe_length'
    ]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix][
        'length_taken_by_holder'
    ]


class Grib_RoTurnMill_T_Z_F2(Grib_RoTurnMill):
    """Describe holder-specific tool parameters.

    T_Z_F2_
    HOLDER_AXIS_EWS_135834
    """

    holder_prefix = 'T_Z_F2_'
    family_name = 'T_Z_F2_SIDE_RO'
    instance_name = 'T_Z_F2_SIDE_RO'
    holder_name = 'HOLDER_AXIS_EWS_135834'
    tail_name = 'SIDE_RO_TAIL'
    cutter_name = 'SIDE_RO_CUT'
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
