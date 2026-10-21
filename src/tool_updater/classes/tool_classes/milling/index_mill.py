from src.tool_updater import config
import json
import logging
from math import pi

from src.tool_updater.classes.tool_classes.base_tool import BaseTool

logger = logging.getLogger(__name__)


class IndexMill(BaseTool):
    # MANUAL TOOL DATA
    tool_material_manual = "Carbide inserts"
    tool_type = "MILLING"

    finishing_roughing_options = {
        "roughing": {
            "vc_modifier": 0.7,  # Множитель для подачи (и на зуб, и на оборот)
            "feed_rate_multiplier": 1,  # Множитель для скорости резания
        },
        "finishing": {
            "vc_modifier": 0.85,
            "feed_rate_multiplier": 0.8,
        },
    }

    # key_ae = "Ae"
    # key_holder_size = "holder_name"

    axial_depth_modifiyers = {
        "iso_P": 0.5,
        "iso_M": 0.4,
        "iso_K": 1,
        "iso_N": 1,
        "iso_S": 1,
        "iso_H": 1,
    }
    radial_depth_modifiyers = {
        "iso_P": 0.65,
        "iso_M": 0.65,
        "iso_K": 0.65,
        "iso_N": 0.65,
        "iso_S": 0.65,
        "iso_H": 0.65,
    }

    path_to_holder_geometry_catalog = (
        config.CATALOGS_DIR / 'milling' / 'index_mills'
        / 'holders_Dandrea.json'
    )

    def __init__(self,
                 tool_size_from_geom_catalogue: str,
                 catalog_tool_cut_data: dict,
                 catalog_tool_geometry: dict,
                 teeth_num: int,
                 file_name_prefix: str,
                 file_name_suffix: str,
                 debug_mode: int,
                 **kwargs):
        self.tool_name_from_input = tool_size_from_geom_catalogue

        self.catalog_tool_cut_data = catalog_tool_cut_data
        self.catalog_tool_geometry = catalog_tool_geometry
        self.teeth_num = teeth_num
        self.file_name_prefix = file_name_prefix
        self.file_name_suffix = file_name_suffix
        self.debug_mode = debug_mode

        with self.path_to_holder_geometry_catalog.open(encoding='utf-8') as f:
            self.catalog_holder_geometry = json.load(f)

        super().__init__(
            tool_size_from_geom_catalogue=self.tool_name_from_input,
            # tool_size_from_geom_catalogue=self.tool_size_from_geom_catalogue,
            catalog_tool_cut_data=self.catalog_tool_cut_data,
            catalog_tool_geometry=self.catalog_tool_geometry,
            teeth_num=self.teeth_num,
            file_name_prefix=self.file_name_prefix,
            file_name_suffix=self.file_name_suffix,
            debug_mode=self.debug_mode,
        )
        self.tool_data["CORNER_RADIUS"] = self.get_tool_corner_radius()
        self.tool_data["SHANK_DIAM"] = self.get_tool_shank_diam()
        self.tool_data["HOLDER_LEN"] = self.get_holder_len()
        self.get_tool_teeth_num()

    def get_tool_corner_radius(self):
        try:
            insert_name = self.catalog_tool_geometry[self.tool_name_from_input]["insert_name"]
            r = self.catalog_tool_cut_data[insert_name]["RE"]
            return r
        except KeyError:
            return 0

    def get_tool_shank_diam(self):
        return self.catalog_tool_geometry[self.tool_name_from_input]["SHANK_DIAM"]

    def get_cutter_diam(self):
        d = self.catalog_tool_geometry[self.tool_name_from_input]["CUTTER_DIAM"]
        return d

    def get_tool_diam_float(self):
        d = self.catalog_tool_geometry[self.tool_name_from_input]["CUTTER_DIAM"]
        return d

    def calc_axial_depth(self, key_iso_material) -> float:
        insert_name = self.catalog_tool_geometry[self.tool_name_from_input]["insert_name"]
        ap = self.catalog_tool_cut_data[insert_name]["Ap"][0]
        return ap * self.axial_depth_modifiyers[key_iso_material]

    def calc_radial_depth(self, key_iso_material):
        # return self.tool_data["CUTTER_DIAM"] * self.radial_depth_modifiyers[key_iso_material]
        insert_name = self.catalog_tool_geometry[self.tool_name_from_input]["insert_name"]
        ae = self.catalog_tool_cut_data[insert_name]["Ae"][0]
        return ae * self.tool_data["CUTTER_DIAM"]
        # return ae * self.axial_depth_modifiyers[key_iso_material]
        # return self.tool_data["CUTTER_DIAM"] * self.radial_depth_modifiyers[key_iso_material]

    # def get_holder_len(self):
    #     hol_size = self.get_tool_holder_size()
    #     l = self.catalog_holder_geometry[hol_size]["holder_len"]
    #     return l

    def get_tool_holder_data(self) -> dict:
        shank_diam = self.get_tool_shank_diam()
        if 50 >= shank_diam > 32:
            return self.catalog_holder_geometry["MAS403 BT40-AD+B MF50"]
        elif 32 >= shank_diam > 20:
            return self.catalog_holder_geometry["MAS403 BT40-AD+B MF32.140"]
        elif 20 >= shank_diam > 12:
            return self.catalog_holder_geometry["MAS403 BT40-AD+B MF20.100"]
        elif 12 >= shank_diam > 0:
            return self.catalog_holder_geometry["MAS403 BT40-AD+B MF12.100"]
        else:
            return self.catalog_holder_geometry["MAS403 BT40-AD+B MF200"]

    def get_holder_len(self):
        return self.get_tool_holder_data()["holder_len"]

    def get_full_tool_length(self) -> float:
        full_tool_len = self.catalog_tool_geometry[self.tool_name_from_input]["LENGTH"]
        return full_tool_len

    def calc_len_out_of_holder(self):
        hol_depth = self.get_tool_holder_data()["max_shank_insertion_depth"]
        hol_body_min_len = self.get_full_tool_length() - hol_depth
        if hol_body_min_len <= 0:
            return 50
        return hol_body_min_len

    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA

    def create_tool_name_for_geom_catalogue(self):
        t_name = self.tool_data["tool_name_str"]
        return t_name

    def create_tool_name_for_cut_catalogue(self):
        return self.catalog_tool_geometry[self.tool_name_from_input]["insert_name"]

    def create_tool_name_for_xml(self):
        t_prefix = self.tool_data["file_name_prefix"].upper()
        t_suffix = self.tool_data["file_name_suffix"].upper()
        d = self.clear_str_from_trailing_zeros(
            str(self.tool_data["CUTTER_DIAM"]), sep=".").replace(".", "-")
        l1 = self.clear_str_from_trailing_zeros(
            str(self.calc_len_out_of_holder()), sep=".").replace(".", "-")
        l2 = self.clear_str_from_trailing_zeros(
            str(self.get_full_tool_length()), sep=".").replace(".", "-")

        t_name = (
            f"{t_prefix}"
            f"D{d}"
            f"_Z{self.get_tool_teeth_num()}"
            f"_L{l1}"
            f"_L{l2}"
            f"_{self.tool_name_from_input.replace(" ", "_")}"
            # f"{t_suffix}"
        )

        return t_name

    def create_file_name(self):
        t_prefix = self.tool_data["file_name_prefix"]
        t_suffix = self.tool_data["file_name_suffix"]

        d = self.clear_str_from_trailing_zeros(
            str(self.tool_data["CUTTER_DIAM"]), sep=".")
        l1 = self.clear_str_from_trailing_zeros(
            str(self.calc_len_out_of_holder()), sep=".")
        l2 = self.clear_str_from_trailing_zeros(
            str(self.get_full_tool_length()), sep=".")

        t_name = (
            f"{t_prefix}"
            f"D{d}"
            f"_Z{self.get_tool_teeth_num()}"
            f"_L{l1}"
            f"_L{l2}"
            f"_({self.tool_name_from_input})"
            f"{t_suffix}"
        )

        return t_name

    def get_tool_flute_length(self) -> float:
        return self.catalog_tool_geometry[self.tool_name_from_input]["FLUTE_LENGTH"]

    def get_tool_teeth_num(self):
        return self.catalog_tool_geometry[self.tool_name_from_input]["NUM_OF_TEETH"]

    def get_tool_comment(self) -> str:
        try:
            t_name = self.tool_name_from_input
            insert_name = self.catalog_tool_geometry[self.tool_name_from_input]["insert_name"]
            return t_name + " + " + insert_name
        except KeyError:
            # logger.warning(f"{self.tool_data["tool_name_str"]} - Tool flute len not found")
            return ""

    def has_cutting_data(self, material: str) -> bool:
        """Check material availability for the selected insert."""
        insert = self.catalog_tool_geometry[self.tool_name_from_input]['insert_name']
        return material in self.catalog_cut_data[insert]['Vc']

    def get_vc(self, key_iso_material: str, fin_or_rough):
        try:
            insert_name = self.catalog_tool_geometry[self.tool_name_from_input]["insert_name"]
            vc_data = self.catalog_cut_data[insert_name]["Vc"][key_iso_material]
            if type(vc_data) is int or type(vc_data) is float:
                vc_data *= self.finishing_roughing_options[fin_or_rough]["vc_modifier"]
                return vc_data
            if type(vc_data) is list or type(vc_data) is set or type(vc_data) is tuple:
                vc_data = vc_data[config.vc_min_or_max]
                vc_data *= self.finishing_roughing_options[fin_or_rough]["vc_modifier"]
                vc_data = round(vc_data, ndigits=config.NDIGITS_SURFACE_SPEED)
                return vc_data
        except KeyError as exc:
            raise ValueError(
                f'Invalid insert cutting data for {key_iso_material}'
            ) from exc

    # def calc_cut_data_for_all_material_groups(self):
    #     for key_iso_material in config.lst_of_iso_material_groups:
    #         for fin_or_rough in self.finishing_roughing_options:
    #             tool_surface_speed = self.get_vc(
    #                 key_iso_material=key_iso_material, fin_or_rough=fin_or_rough)
    #             tool_spindle_rpm = self.calc_rpm(Vc=tool_surface_speed)

    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough][
    #                 "TOOL_SURFACE_SPEED"] = tool_surface_speed
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"] = tool_spindle_rpm

    #             tool_feed_per_unit = self.calc_feed_per_unit(key_iso_material=key_iso_material,
    #                                                          fin_or_rough=fin_or_rough)
    #             tool_feed_rate = self.calc_feed_rate(key_iso_material=key_iso_material, RPM=tool_spindle_rpm,
    #                                                  fin_or_rough=fin_or_rough)
    #             tool_axial_depth = self.calc_axial_depth(
    #                 key_iso_material=key_iso_material)
    #             tool_radial_depth = self.calc_radial_depth(
    #                 key_iso_material=key_iso_material)

    #             multiplyer = 1
    #             if tool_spindle_rpm >= config.MAX_RPM:
    #                 multiplyer = config.MAX_RPM / tool_spindle_rpm
    #                 self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"] = round(
    #                     tool_spindle_rpm * multiplyer, ndigits=config.NDIGITS_SPINDLE)
    #                 self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SURFACE_SPEED"] = round(
    #                     tool_surface_speed * multiplyer, ndigits=config.NDIGITS_SURFACE_SPEED)

    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_PER_UNIT"] = round(
    #                 tool_feed_per_unit * multiplyer, ndigits=config.NDIGITS_FEED_PER_UNIT)
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_RATE"] = round(
    #                 tool_feed_rate * multiplyer, ndigits=config.NDIGITS_FEED)
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_AXIAL_DEPTH"] = round(
    #                 tool_axial_depth * multiplyer, ndigits=config.NDIGITS_AXIAL_FEED)
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_RADIAL_DEPTH"] = round(
    #                 tool_radial_depth * multiplyer, ndigits=config.NDIGITS_RADIAL_FEED)

    # def calc_cut_data_for_all_material_groups(self):
    #     for key_iso_material in config.lst_of_iso_material_groups:
    #         for fin_or_rough in self.finishing_roughing_options:
    #             tool_surface_speed = self.get_vc(
    #                 key_iso_material=key_iso_material, fin_or_rough=fin_or_rough)
    #             tool_spindle_rpm = self.calc_rpm(Vc=tool_surface_speed)

    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough][
    #                 "TOOL_SURFACE_SPEED"] = tool_surface_speed
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"] = tool_spindle_rpm

    #             tool_feed_per_unit = self.calc_feed_per_unit(key_iso_material=key_iso_material,
    #                                                          fin_or_rough=fin_or_rough)
    #             tool_feed_rate = self.calc_feed_rate(key_iso_material=key_iso_material, RPM=tool_spindle_rpm,
    #                                                  fin_or_rough=fin_or_rough)
    #             tool_axial_depth = self.calc_axial_depth(
    #                 key_iso_material=key_iso_material)
    #             tool_radial_depth = self.calc_radial_depth(
    #                 key_iso_material=key_iso_material)

    #             multiplyer = 1
    #             if tool_spindle_rpm >= config.MAX_RPM:
    #                 multiplyer = config.MAX_RPM / tool_spindle_rpm
    #                 self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"] = round(
    #                     tool_spindle_rpm * multiplyer, ndigits=config.NDIGITS_SPINDLE)
    #                 self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SURFACE_SPEED"] = round(
    #                     tool_surface_speed * multiplyer, ndigits=config.NDIGITS_SURFACE_SPEED)

    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_PER_UNIT"] = round(
    #                 tool_feed_per_unit * multiplyer, ndigits=config.NDIGITS_FEED_PER_UNIT)
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_FEED_RATE"] = round(
    #                 tool_feed_rate * multiplyer, ndigits=config.NDIGITS_FEED)
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_AXIAL_DEPTH"] = round(
    #                 tool_axial_depth * multiplyer, ndigits=config.NDIGITS_AXIAL_FEED)
    #             self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_RADIAL_DEPTH"] = round(
    #                 tool_radial_depth * multiplyer, ndigits=config.NDIGITS_RADIAL_FEED)

    def calc_rpm(self, Vc: int | float) -> float:
        rpm = 1000 * Vc / (pi * self.tool_data["tool_diam_float"])
        return round(rpm, ndigits=config.NDIGITS_SPINDLE)

    # def calc_feed_per_unit(self, key_iso_material, fin_or_rough: str) -> float:
    #     try:
    #         feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
    #         F = self.catalog_cut_data[key_iso_material][config.key_f][self.tool_data["cut_data_diam_group"]]
    #         RPM = self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"]
    #         fz = F / RPM / self.tool_data["NUM_OF_TEETH"] * feed_multiplier
    #         return round(fz, ndigits=config.NDIGITS_FEED_PER_UNIT)
    #     except:
    #         #             logger.critical(f"{self.tool_data["tool_name_str"]} - feed per unit not calculated")
    #         return 0

    def calc_feed_per_unit(self, key_iso_material, fin_or_rough):
        insert_name = self.catalog_tool_geometry[self.tool_name_from_input]["insert_name"]
        Fz_min = self.catalog_cut_data[insert_name]["Fz"][0]
        Fz_max = self.catalog_cut_data[insert_name]["Fz"][1]
        Fz = (Fz_max + Fz_min) / 2
        return Fz

    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
        Fz = self.calc_feed_per_unit(key_iso_material, fin_or_rough)
        z = self.catalog_tool_geometry[self.tool_name_from_input]["NUM_OF_TEETH"]
        F = Fz * z * RPM * feed_multiplier
        return round(F, ndigits=config.NDIGITS_FEED)

    def get_asm_name_for_xml(self):
        return self.catalog_tool_geometry[self.tool_name_from_input]["asm_name"]

    def get_body_name_for_xml(self):
        return self.catalog_tool_geometry[self.tool_name_from_input]["body_prt_name"]

    def get_insert_prt_name_for_xml(self):
        return self.catalog_tool_geometry[self.tool_name_from_input]["insert_prt_name"]

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <ModelInfo InstanceName="INDEX_MILL_ASM" Type="Assembly"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_RADIUS"]}"/>
            <MfgParam Name="SIDE_ANGLE" Value="{0}"/>
            <MfgParam Name="SHANK_DIAM" Value="{self.tool_data["SHANK_DIAM"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_DIA_MIN" Value="{self.get_tool_holder_data()["holder_min_diam"]}"/>
            <MfgParam Name="HOLDER_DIA_MAX" Value="{self.get_tool_holder_data()["holder_max_diam"]}"/>
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
        logger.debug(
            f"{self.tool_name_from_input} - xml_tool_params generated...")
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

        logger.debug(
            f"{self.tool_name_from_input} - xml_tool_cut_data generated...")
        return total_string

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
            <BOM>
                <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40_HOLDER" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="INDEX_MILL_TAIL" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="INDEX_MILL_CUTTER" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(
            f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str


class IndexMillSingleASMs(IndexMill):

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            <ModelInfo InstanceName="{self.get_asm_name_for_xml()}" Type="Assembly"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_RADIUS"]}"/>
            <MfgParam Name="SIDE_ANGLE" Value="{0}"/>
            <MfgParam Name="SHANK_DIAM" Value="{self.tool_data["SHANK_DIAM"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_DIA_MIN" Value="{self.get_tool_holder_data()["holder_min_diam"]}"/>
            <MfgParam Name="HOLDER_DIA_MAX" Value="{self.get_tool_holder_data()["holder_max_diam"]}"/>
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
        logger.debug(
            f"{self.tool_name_from_input} - xml_tool_params generated...")
        return xml_part_str

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
                <BOM>
                    <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="BT40_HOLDER" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.get_body_name_for_xml()}" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.get_insert_prt_name_for_xml()}" Quantity="{self.tool_data["NUM_OF_TEETH"]}" Type="GENERAL"/>
                </BOM>
    """
        logger.debug(
            f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str


# class IndexMillTaeguTec3PTE90_10(IndexMill):
#
#
#     def set_xml_body_tool_params(self) -> str:
#         xml_part_str = f"""\
#     <ToolingSetup>
#         <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
#             <Attr DataType="boolean" Name="UseOutline" Value="false"/>
#             <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
#             <Attr DataType="boolean" Name="SketchTool" Value="false"/>
#             <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
#             <ModelInfo InstanceName="{self.get_asm_name_for_xml()}" Type="Assembly"/>
#             <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
#             <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
#             <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
#             <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_RADIUS"]}"/>
#             <MfgParam Name="SIDE_ANGLE" Value="{0}"/>
#             <MfgParam Name="SHANK_DIAM" Value="{self.tool_data["SHANK_DIAM"]}"/>
#             <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
#             <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
#             <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
#             <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
#             <MfgParam Name="HOLDER_DIA_MIN" Value="{self.get_tool_holder_data()["holder_min_diam"]}"/>
#             <MfgParam Name="HOLDER_DIA_MAX" Value="{self.get_tool_holder_data()["holder_max_diam"]}"/>
#             <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>
#             <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
#             <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
#             <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
#             <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
#             <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
#             <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
#             <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
#             <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
#     """
#         logger.debug(f"{self.tool_name_from_input} - xml_tool_params generated...")
#         return xml_part_str
#
#     def set_xml_bom_components(self) -> str:
#         xml_part_str = f"""\
#                 <BOM>
#                     <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
#                     <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
#                     <BOMComponent Comments=" " Name="BT40_HOLDER" Quantity="1" Type="HOLDER"/>
#                     <BOMComponent Comments=" " Name="{self.get_body_name_for_xml()}" Quantity="1" Type="HOLDER"/>
#                     <BOMComponent Comments=" " Name="{self.get_insert_prt_name_for_xml()}" Quantity="{self.tool_data["NUM_OF_TEETH"]}" Type="GENERAL"/>
#                 </BOM>
#     """
#         logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
#         return xml_part_str
#
