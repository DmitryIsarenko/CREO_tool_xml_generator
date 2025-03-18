from src.tool_updater import config
import logging

from src.tool_updater.classes.tool_classes.base_tool import BaseTool

logger = logging.getLogger(__name__)


class ChamferMill(BaseTool):
    # MANUAL TOOL DATA
    tool_material_manual = "VHM"
    # tool_type = "TAPER MILL"
    tool_type = "MILLING"

    finishing_roughing_options = {
        "roughing": {
            "vc_modifier": 1,  # Множитель для подачи (и на зуб, и на оборот)
            "feed_rate_multiplier": 0.6,  # Множитель для скорости резания
        },
        "finishing": {
            "vc_modifier": 1,
            "feed_rate_multiplier": 0.6,
        },
    }

    axial_depth_modifiyers = {
        "iso_P": 0.3,
        "iso_M": 0.3,
        "iso_K": 0.3,
        "iso_N": 0.3,
        "iso_S": 0.3,
        "iso_H": 0.3,
    }
    radial_depth_modifiyers = {
        "iso_P": 0.15,
        "iso_M": 0.1,
        "iso_K": 0.1,
        "iso_N": 0.2,
        "iso_S": 0.1,
        "iso_H": 0.025,
    }

    def __init__(self,
                 tool_size_from_geom_catalogue: str,
                 catalog_tool_cut_data: dict,
                 catalog_tool_geometry: dict,
                 teeth_num: int,
                 file_name_prefix: str,
                 file_name_suffix: str,
                 debug_mode: int,
                 **kwargs):
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

    def get_shank_diam(self):
        return self.catalog_tool_geometry[self.complex_size_name]["flute_diam"]

    def get_tip_diam(self):
        try:
            return self.catalog_tool_geometry[self.complex_size_name]["tip_diam"]
        except:
            return 0.2

    def get_corner_radius(self):
        return 0

    def get_side_angle(self):
        return self.catalog_tool_geometry[self.complex_size_name]["side_angle"]

    def calc_len_out_of_holder(self):
        hol_len = self.catalog_tool_geometry[self.complex_size_name]["full_body_len"]
        flute_len = self.catalog_tool_geometry[self.complex_size_name]["flute_len"]
        return hol_len - 25

    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA
    def create_tool_name_for_geom_catalogue(self):
        t_name = self.tool_data["tool_name_str"]
        return t_name

    def create_tool_name_for_cut_catalogue(self):
        t_name = self.tool_data["tool_diam_float"]
        return t_name

    def create_tool_name_for_xml(self):
        t_prefix = self.tool_data["file_name_prefix"].upper()
        t_suffix = self.tool_data["file_name_suffix"].upper()

        d = self.clear_str_from_trailing_zeros(str(self.tool_data["CUTTER_DIAM"]), sep=".").replace(".", "-")
        angle = self.clear_str_from_trailing_zeros(str(self.get_side_angle() * 2), sep=".").replace(".", "-")
        l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".").replace(".", "-")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".").replace(".", "-")

        t_name = (
            f"{t_prefix}"
            f"D{d}"
            f"x{angle}"
            f"_L{l1}"
            f"-L{l2}"
            # f"{t_suffix}"
        )
        return t_name

    def create_file_name(self):
        t_prefix = self.tool_data["file_name_prefix"]
        t_suffix = self.tool_data["file_name_suffix"]

        d = self.clear_str_from_trailing_zeros(str(self.tool_data["CUTTER_DIAM"]), sep=".")
        angle = self.get_side_angle() * 2
        l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".")

        t_name = (
            f"{t_prefix}"
            f"D{d}"
            f"x{angle}"
            f"_L{l1}"
            f"-L{l2}"
            f"{t_suffix}"
        )
        return t_name

    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        try:
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            F = self.catalog_cut_data[key_iso_material][config.key_f][self.tool_data["cut_data_diam_group"]]
            F *= feed_multiplier
            return round(F, ndigits=config.NDIGITS_FEED)
        except:
            # logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <ModelInfo FamilyName="CHAMFER_MILL_ASM" InstanceName="CHAMFER_MILL_ASM{self.d_for_bom()}" Type="Assembly"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="SHANK_DIAM" Value="{self.shank_diam}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tip_diam}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.corner_radius}"/>
            <MfgParam Name="SIDE_ANGLE" Value="{self.side_angle}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="CUT_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
    """
        logger.debug(f"{self.complex_size_name} - xml_tool_params generated...")
        return xml_part_str

    def set_xml_body_tool_cut_data(self):
        total_string = ""
        for material_name, mat_iso_name in config.mfg_materials_dict.items():
            xml_part_str = f"""\
        <ToolCutData>
                <Material>
                    <MfgParam Name="STOCK_MATERIAL" Value="{material_name}"/>
                </Material>
                <CutDataUnitSystem>
                    <MfgParam Name="CUT_DATA_UNITS" Value="METRIC"/>
                </CutDataUnitSystem>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="ROUGHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_AXIAL_DEPTH"]}"/>
                    <MfgParam Name="TOOL_RADIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_RADIAL_DEPTH"]}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_tooth" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                    <MfgParam Name="TOOL_RADIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_RADIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
        """
            total_string += xml_part_str

        logger.debug(f"{self.complex_size_name} - xml_tool_cut_data generated...")
        return total_string



    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
            <BOM>
                <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40_HOLDER{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="CHAMFER_MILL_TAIL{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="CHAMFER_MILL_CUTTER{self.d_for_bom()}" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str
