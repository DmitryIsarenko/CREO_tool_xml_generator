from src.tool_updater import config
from math import ceil
import logging


from src.tool_updater.classes.tool_classes.base_tool import BaseTool
from src.tool_updater.classes.turnmill_len_adaptors import adapt_length, adapt_flute_length
from src.tool_updater.config import turnmill_holders_safe_lengths

logger = logging.getLogger(__name__)


class ToroidMill(BaseTool):
    # MANUAL TOOL DATA
    tool_material_manual = "VHM"
    tool_type = "BULL MILL"

    finishing_roughing_options = {
        "roughing": {
            "vc_modifier": 1,  # Множитель для подачи (и на зуб, и на оборот)
            "feed_rate_multiplier": 0.6,  # Множитель для скорости резания
        },
        "finishing": {
            "vc_modifier": 1.2,
            "feed_rate_multiplier": 0.4,
        },
    }

    axial_depth_modifiyers = {
        "iso_P": 1.5,
        "iso_M": 1.5,
        "iso_K": 1.5,
        "iso_N": 1.5,
        "iso_S": 1.5,
        "iso_H": 1.5,
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
        self.tool_data["CORNER_RADIUS"] = self.get_tool_corner_rad_from_complex_size()

    def get_tool_flute_diam_from_complex_size(self):
        return self.complex_size_name.split(sep=" R")[0]

    def get_tool_corner_rad_from_complex_size(self):
        return self.complex_size_name.split(sep=" R")[1]

    def get_tool_diam_float(self):
        return float(self.get_tool_flute_diam_from_complex_size())

    def get_cutter_diam(self):
        return self.get_tool_flute_diam_from_complex_size()

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
        l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".").replace(".", "-")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".").replace(".", "-")
        r = self.clear_str_from_trailing_zeros(str(self.get_tool_corner_rad_from_complex_size()), sep=".").replace(".",
                                                                                                                   "-")

        t_name = (
            f"{t_prefix}"
            f"D{d}"
            f"_R{r}"
            f"_L{l1}"
            f"-L{l2}"
            # f"{t_suffix}"
        )
        return t_name

    def create_file_name(self):
        t_prefix = self.tool_data["file_name_prefix"]
        t_suffix = self.tool_data["file_name_suffix"]

        d = self.clear_str_from_trailing_zeros(str(self.tool_data["CUTTER_DIAM"]), sep=".")
        l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".")
        r = self.clear_str_from_trailing_zeros(str(self.get_tool_corner_rad_from_complex_size()), sep=".")

        t_name = (
            f"{t_prefix}"
            f"D{d}"
            f"_R{r}"
            f"_L{l1}"
            f"-L{l2}"
            f"{t_suffix}"
        )
        return t_name

    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
        F = self.catalog_cut_data[key_iso_material][config.key_f][self.tool_data["cut_data_diam_group"]]
        F *= feed_multiplier
        return round(F, ndigits=config.NDIGITS_FEED)

    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            
            <ModelInfo FamilyName="TOROID_MILL_ASM" InstanceName="TOROID_MILL_ASM{self.d_for_bom()}" Type="Assembly"/>
            
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_RADIUS"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>
            
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>
            
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
    """
        logger.debug(f"xml_tool_params generated...")
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

        logger.debug(f"xml_tool_cut_data generated...")
        return total_string

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
            <BOM>
                <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40_HOLDER{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="TOROID_MILL_TAIL{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="TOROID_MILL_CUTTER{self.d_for_bom()}" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str



class ToroidTurnMill(ToroidMill):
    holder_prefix = "TM_X_"
    family_name = "TM_X_TOROID_ASM"
    instance_name = "TM_X_TOROID_ASM"
    holder_name = "AXIAL_KOROTKY_EWS_107605"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]

    def d_for_bom(self) -> str:
        """
        возвращает запись в виде _Dxx-x, округленную в большую сторону с точностью до
        0.1 - 20.00 - до 0.1мм
        20.50 - 30.00 - до 0.5мм
        31 - 50 - до 1мм
        55 - 100 до 5мм
        110 - 200 - до 10мм
        220 - 600 - до 20мм
        :return:
        """
        diam_float = float(self.tool_data["CUTTER_DIAM"])

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

        if "." in diam_formatted:
            diam_formatted = diam_formatted.replace(".", "-")
        else:
            diam_formatted = diam_formatted + "-0"

        if len(diam_formatted.split("-")[1]) == 1:
            # diam_formatted += "0"
            pass
        elif len(diam_formatted.split("-")[1]) > 1:
            diam_formatted = diam_formatted[0:5:1]

        return "_D" + diam_formatted

    def adapt_drill_lengths(self):
        self.tool_data["len_out_of_holder"] = adapt_length(
            max_safe_length=self.max_safe_length,
            length_taken_by_holder=self.length_taken_by_holder,
            default_full_length=self.tool_data["len_out_of_holder"]
        )
        self.tool_data["FLUTE_LENGTH"] = adapt_flute_length(
            default_flute_length=self.tool_data["FLUTE_LENGTH"],
            full_length_adapted=self.tool_data["len_out_of_holder"]
        )

    def set_xml_body_tool_params(self) -> str:
        self.adapt_drill_lengths()
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>

            <ModelInfo FamilyName="{self.family_name}" InstanceName="{self.instance_name}{self.d_for_bom()}" Type="Assembly"/>

            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="CORNER_RADIUS" Value="{self.tool_data["CORNER_RADIUS"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            <MfgParam Name="NUM_OF_TEETH" Value="{self.tool_data["NUM_OF_TEETH"]}"/>

            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>

            <MfgParam Name="SCP_TO_TAP_LEN" Value="{self.length_taken_by_holder}"/>
            <MfgParam Name="SAFE_LENGTH" Value="{self.max_safe_length}"/>

            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
        """
        # logger.debug(f"{self.tool_size_from_geom_catalogue} - xml_tool_params generated...")
        return xml_part_str

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
                <BOM>
                    <BOMComponent Comments=" " Name="{self.holder_name}" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.tail_name}{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.cutter_name}{self.d_for_bom()}" Quantity="1" Type="GENERAL"/>
                </BOM>
    """
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str


class ToroidTurnMill_TM_X(ToroidTurnMill):
    """
    TM_X_
    AXIAL_KOROTKY_EWS_107605
    """

    holder_prefix = "TM_X_"
    family_name = "TM_X_TOROID"
    instance_name = "TM_X_TOROID"
    holder_name = "AXIAL_KOROTKY_EWS_107605"
    tail_name = "TOROID_TAIL"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]

    cutter_name = "TOROID_CUT"


class ToroidTurnMill_TM_X_L(ToroidTurnMill):
    """
    TM_X_L_
    AXIAL_EWS_234762
    """
    holder_prefix = "TM_X_L_"
    family_name = "TM_X_L_TOROID"
    instance_name = "TM_X_L_TOROID"
    holder_name = "AXIAL_EWS_234762"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class ToroidTurnMill_TM_Z_1(ToroidTurnMill):
    """
    TM_Z_1_
    RADIAL_1_EWS_195136
    """
    holder_prefix = "TM_Z_1_"
    family_name = "TM_Z_1_TOROID"
    instance_name = "TM_Z_1_TOROID"
    holder_name = "RADIAL_1_EWS_195136"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class ToroidTurnMill_TM_Z_2(ToroidTurnMill):
    """
    TM_Z_2_
    RADIAL_2_EWS_196914
    """
    holder_prefix = "TM_Z_2_"
    family_name = "TM_Z_2_TOROID"
    instance_name = "TM_Z_2_TOROID"
    holder_name = "RADIAL_2_EWS_196914"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class ToroidTurnMill_TM_Z_SUB(ToroidTurnMill):
    """
    TM_Z_SUB_
    RADIAL_2_EWS_196914
    """
    holder_prefix = "TM_Z_SUB_"
    family_name = "TM_Z_SUB_TOROID"
    instance_name = "TM_Z_SUB_TOROID"
    holder_name = "RADIAL_2_EWS_196914"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class ToroidTurnMill_T_Z_ER(ToroidTurnMill):
    """
    T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """
    holder_prefix = "T_Z_ER_"
    family_name = "T_Z_ER_TOROID"
    instance_name = "T_Z_ER_TOROID"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "TOROID_TAIL"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]

    cutter_name = "TOROID_CUT"

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
                <BOM>
                    <BOMComponent Comments=" " Name="{self.holder_name}" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.tail_name}{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="HOLDER_COLLETS" Quantity="2" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.cutter_name}{self.d_for_bom()}" Quantity="1" Type="GENERAL"/>
                </BOM>
    """
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str


class ToroidTurnMill_T_Z_SUB_ER(ToroidTurnMill):
    """
    T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """
    holder_prefix = "T_Z_SUB_ER_"
    family_name = "T_Z_SUB_ER_TOROID"
    instance_name = "T_Z_SUB_ER_TOROID"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "TOROID_TAIL"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]

    cutter_name = "TOROID_CUT"

    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
                <BOM>
                    <BOMComponent Comments=" " Name="{self.holder_name}" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.tail_name}{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="HOLDER_COLLETS" Quantity="2" Type="HOLDER"/>
                    <BOMComponent Comments=" " Name="{self.cutter_name}{self.d_for_bom()}" Quantity="1" Type="GENERAL"/>
                </BOM>
    """
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str


class ToroidTurnMill_T_Z(ToroidTurnMill):
    """
    T_Z_
    HOLDER_L85_S02361
    """
    holder_prefix = "T_Z_"
    family_name = "T_Z_TOROID"
    instance_name = "T_Z_TOROID"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class ToroidTurnMill_T_Z_SUB(ToroidTurnMill):
    """
    T_Z_SUB_
    HOLDER_L85_S02361
    """
    holder_prefix = "T_Z_SUB_"
    family_name = "T_Z_SUB_TOROID"
    instance_name = "T_Z_SUB_TOROID"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class ToroidTurnMill_T_Z_F2(ToroidTurnMill):
    """
    T_Z_F2_
    HOLDER_AXIS_EWS_135834
    """
    holder_prefix = "T_Z_F2_"
    family_name = "T_Z_F2_TOROID"
    instance_name = "T_Z_F2_TOROID"
    holder_name = "HOLDER_AXIS_EWS_135834"
    tail_name = "TOROID_TAIL"
    cutter_name = "TOROID_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


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