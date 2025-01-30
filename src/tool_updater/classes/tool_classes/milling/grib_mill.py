from src.tool_updater import config
import json
import logging

from src.tool_updater.classes.tool_classes.base_tool import BaseTool

logger = logging.getLogger(__name__)


class GribMillFlat(BaseTool):
    # MANUAL TOOL DATA
    tool_material_manual = "Carbide inserts"
    tool_type = "SIDE_MILLING"

    finishing_roughing_options = {
        "roughing": {
            "vc_modifier": 1,  # Множитель для подачи (и на зуб, и на оборот)
            "feed_rate_multiplier": 0.6,  # Множитель для скорости резания
        },
        "finishing": {
            "vc_modifier": 1.1,
            "feed_rate_multiplier": 0.5,
        },
    }

    key_ae = "Ae"
    key_holder_size = "holder_name"

    axial_depth_modifiyers = {
        "iso_P": 1,
        "iso_M": 1,
        "iso_K": 1,
        "iso_N": 1,
        "iso_S": 1,
        "iso_H": 1,
    }
    radial_depth_modifiyers = {
        "iso_P": 1,
        "iso_M": 1,
        "iso_K": 1,
        "iso_N": 1,
        "iso_S": 1,
        "iso_H": 1,
    }

    path_to_holder_geometry_catalog = r"C:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\holders_for_MultiMaster.json"

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

        with open(self.path_to_holder_geometry_catalog, mode="r") as f:
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
        self.tool_data["CORNER_RADIUS"] = self.get_tool_corner_radius_from_complex_size()
        self.tool_data["CORNER_CHAMFER"] = self.get_tool_corner_chamfer_from_complex_size()
        self.tool_data["CORNER_CHAMFER_ANGLE"] = self.get_tool_corner_chamfer_angle_from_complex_size()
        self.tool_data["CUTTER_WIDTH"] = self.get_tool_cutter_width_from_complex_size()
        self.tool_data["SHANK_DIAM"] = self.get_tool_shank_diam()

    def get_tool_flute_diam_from_complex_size(self):
        return self.complex_size_name.split(sep=" ")[0]

    def get_tool_cutter_width_from_complex_size(self):
        w = self.complex_size_name.split(sep=" ")[1].replace("W", "")
        while len(w.split(sep=".")[1]) < 2:
            w += "0"
        return w

    def get_tool_corner_radius_from_complex_size(self):
        return self.complex_size_name.split(sep=" ")[2].replace("R", "")

    def get_tool_corner_chamfer_from_complex_size(self):
        return self.complex_size_name.split(sep=" ")[3].replace("C", "")

    def get_tool_corner_chamfer_angle_from_complex_size(self):
        return self.complex_size_name.split(sep=" ")[4].replace("A", "")

    def get_tool_shank_diam(self):
        hol_size = self.get_tool_holder_size()
        return self.catalog_holder_geometry[hol_size]["lowering_diam"]

    def get_tool_diam_float(self):
        return float(self.get_tool_flute_diam_from_complex_size())

    def get_cutter_diam(self):
        return self.get_tool_flute_diam_from_complex_size()

    def calc_axial_depth(self, key_iso_material) -> float:
        return float(self.get_tool_cutter_width_from_complex_size())

    def calc_radial_depth(self, key_iso_material):
        try:
            return self.catalog_tool_geometry[self.complex_size_name]["max_cut_depth"]
        except:
            return 0

    # def get_holder_len(self):
    #     hol_size = self.get_tool_holder_size()
    #     l = self.catalog_holder_geometry[hol_size]["holder_len"]
    #     return l

    def get_tool_holder_size(self):
        hol_size = self.catalog_tool_geometry[self.complex_size_name][self.key_holder_size]
        return hol_size

    def get_full_tool_length(self) -> float:
        hol_size = self.get_tool_holder_size()
        hol_len = self.catalog_holder_geometry[hol_size]["holder_full_len"]
        return hol_len

    def calc_len_out_of_holder(self):
        hol_size = self.get_tool_holder_size()
        hol_body_min_len = self.catalog_holder_geometry[hol_size]["len_to_lowering_start"]
        return hol_body_min_len

    def calc_feed_per_unit(self, key_iso_material, fin_or_rough):
        try:
            cut_w = self.get_tool_cutter_width_from_complex_size()
            Fz = self.catalog_cut_data[key_iso_material][config.key_fz][cut_w]
            # Fz = str(self.catalog_cut_data[key_iso_material][config.key_fz][cut_w])
            # while len(Fz.split(sep=".")[1]) < 2:
            #     Fz += "0"
            return Fz
        except:
            return 0

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
        d = self.clear_str_from_trailing_zeros(self.tool_data["CUTTER_DIAM"], sep=".").replace(".", "-")
        w = self.clear_str_from_trailing_zeros(self.get_tool_cutter_width_from_complex_size(), sep=".").replace(
            ".", "-")
        r = self.clear_str_from_trailing_zeros(self.get_tool_corner_radius_from_complex_size(), sep=".").replace(
            ".", "-")
        # r = self.get_tool_corner_radius_from_complex_size().replace(".", "-")
        c = self.clear_str_from_trailing_zeros(self.get_tool_corner_chamfer_from_complex_size(), sep=".").replace(
            ".", "-")
        a = self.clear_str_from_trailing_zeros(self.get_tool_corner_chamfer_angle_from_complex_size(), sep=".").replace(
            ".", "-")
        l1 = self.clear_str_from_trailing_zeros(str(self.calc_len_out_of_holder()), sep=".").replace(".", "-")
        l2 = self.clear_str_from_trailing_zeros(str(self.get_full_tool_length()), sep=".").replace(".", "-")
        if r == "0" and c =="0":
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_L{l1}"
                f"_L{l2}"
                # f"{t_suffix}"
            )
        elif r == "0" and c != "0" and a != "0":
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_C{c}"
                f"_A{a}"
                f"_L{l1}"
                f"_L{l2}"
                # f"{t_suffix}"
            )
        elif r != "0" and c == "0":
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_R{r}"
                f"_L{l1}"
                f"_L{l2}"
                # f"{t_suffix}"
            )
        else:
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_R{r}"
                f"_C{c}"
                f"_A{a}"
                f"_L{l1}"
                f"_L{l2}"
                # f"{t_suffix}"
            )

        return t_name

    def create_file_name(self):
        t_prefix = self.tool_data["file_name_prefix"]
        t_suffix = self.tool_data["file_name_suffix"]

        d = self.clear_str_from_trailing_zeros(self.tool_data["CUTTER_DIAM"], sep=".")
        w = self.clear_str_from_trailing_zeros(self.get_tool_cutter_width_from_complex_size(), sep=".")
        # r = self.clear_str_from_trailing_zeros(self.get_tool_corner_radius_from_complex_size(), sep=".")
        r = self.get_tool_corner_radius_from_complex_size()
        c = self.clear_str_from_trailing_zeros(self.get_tool_corner_chamfer_from_complex_size(), sep=".")
        a = self.clear_str_from_trailing_zeros(self.get_tool_corner_chamfer_angle_from_complex_size(), sep=".")
        l1 = self.clear_str_from_trailing_zeros(str(self.calc_len_out_of_holder()), sep=".")
        l2 = self.clear_str_from_trailing_zeros(str(self.get_full_tool_length()), sep=".")

        if r == "0" and c =="0":
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_L{l1}"
                f"_L{l2}"
                f"{t_suffix}"
            )
        elif r == "0" and c != "0" and a != "0":
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_C{c}"
                f"_A{a}"
                f"_L{l1}"
                f"_L{l2}"
                f"{t_suffix}"
            )
        elif r != "0" and c == "0":
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_R{r}"
                f"_L{l1}"
                f"_L{l2}"
                f"{t_suffix}"
            )
        else:
            t_name = (
                f"{t_prefix}"
                f"D{d}"
                f"_W{w}"
                f"_R{r}"
                f"_C{c}"
                f"_A{a}"
                f"_L{l1}"
                f"_L{l2}"
                f"{t_suffix}"
            )
        return t_name

    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        try:
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            Fz = self.catalog_cut_data[key_iso_material][config.key_fz][self.get_tool_cutter_width_from_complex_size()]
            z = self.catalog_tool_geometry[self.complex_size_name][config.key_num_of_teeth]
            F = Fz * z * RPM * feed_multiplier
            return round(F, ndigits=config.NDIGITS_FEED)
        except:
            # logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0

    def get_tool_teeth_num(self):
        try:
            return self.catalog_tool_geometry[self.complex_size_name][config.key_num_of_teeth]
        except:
            return 0

    # def calc_nut_diam(self) -> int:
    #     return self.get_tool_shank_diam() + 20

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <ModelInfo InstanceName="SIDE_MILL_FLAT_ASM" Type="Assembly"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>

            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_RADIUS"]}"/>
            <MfgParam Name="CUTTER_WIDTH" Value="{self.tool_data["CUTTER_WIDTH"]}"/>

            <MfgParam Name="SHANK_DIAM" Value="{self.tool_data["SHANK_DIAM"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>

            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>

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
                <BOMComponent Comments=" " Name="BT40_HOLDER" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="SIDE_MILL_FLAT_TAIL" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="SIDE_MILL_FLAT_CUTTER" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str



class GribMillChamfer(GribMillFlat):

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <ModelInfo InstanceName="SIDE_MILL_CHAMFER_ASM" Type="Assembly"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="CORNER_CHAMFER" Value="{self.tool_data["CORNER_CHAMFER"]}"/>
            <MfgParam Name="CORNER_CHAMFER_ANGLE" Value="{self.tool_data["CORNER_CHAMFER_ANGLE"]}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_CHAMFER"]}"/>
            <MfgParam Name="CUTTER_WIDTH" Value="{self.tool_data["CUTTER_WIDTH"]}"/>
            <MfgParam Name="SHANK_DIAM" Value="{self.tool_data["SHANK_DIAM"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
    """
        logger.debug(f"{self.complex_size_name} - xml_tool_params generated...")
        return xml_part_str

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
            <BOM>
                <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40_HOLDER" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="SIDE_MILL_CHAMFER_TAIL" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="SIDE_MILL_CHAMFER_CUTTER" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str


class GribMillRounding(GribMillFlat):

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <ModelInfo InstanceName="SIDE_MILL_ROUNDING_ASM" Type="Assembly"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_RADIUS"]}"/>
            <MfgParam Name="CORNER_CHAMFER" Value="{self.tool_data["CORNER_CHAMFER"]}"/>
            <MfgParam Name="CORNER_CHAMFER_ANGLE" Value="{self.tool_data["CORNER_CHAMFER_ANGLE"]}"/>
            <MfgParam Name="CUTTER_WIDTH" Value="{self.tool_data["CUTTER_WIDTH"]}"/>
            <MfgParam Name="SHANK_DIAM" Value="{self.tool_data["SHANK_DIAM"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
    """
        logger.debug(f"{self.complex_size_name} - xml_tool_params generated...")
        return xml_part_str

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
            <BOM>
                <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40_HOLDER" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="SIDE_MILL_ROUNDING_TAIL" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="SIDE_MILL_ROUNDING_CUTTER" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str
