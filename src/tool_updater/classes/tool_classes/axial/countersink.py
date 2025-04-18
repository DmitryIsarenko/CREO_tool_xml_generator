from src.tool_updater import config
import logging
from math import ceil

from tool_updater.classes.turnmill_len_adaptors import adapt_length, adapt_flute_length
from tool_updater.config import turnmill_holders_safe_lengths

from src.tool_updater.classes.tool_classes.base_tool import BaseTool
from tool_updater.classes.tool_renamer import suffix

logger = logging.getLogger(__name__)


class CounterSink(BaseTool):
    # MANUAL TOOL DATA
    tool_material_manual = "HSS"
    tool_type = "COUNTERSINK"
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
        "iso_P": 1,
        "iso_M": 1,
        "iso_K": 1,
        "iso_N": 1,
        "iso_S": 1,
        "iso_H": 1,
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
        self.point_diameter = self.get_tool_point_diameter()
        self.set_tool_xml()

    # FORMATTING RECENTLY EXISTING/EXTRACTED DATA
    def create_tool_name_for_geom_catalogue(self):
        t_name = self.tool_data["tool_name_str"]
        return t_name

    def create_tool_name_for_cut_catalogue(self):
        t_name = self.tool_data["tool_diam_float"]
        return t_name

    def create_file_name(self):
        real_fl_len = (float(self.tool_data["CUTTER_DIAM"]) - self.get_tool_point_diameter()) / 2
        real_fl_len = self.clear_str_from_trailing_zeros(str(real_fl_len), sep=".")
        d = self.clear_str_from_trailing_zeros(str(self.tool_data["CUTTER_DIAM"]), sep=".")

        # l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".")

        t_name = (
            f"{self.file_name_prefix}"
            f"D{d}"
            f"_L{real_fl_len}"
            f"_L{l2}"
            f"{self.file_name_suffix}"
        )
        return t_name

    def create_tool_name_for_xml(self):
        real_fl_len = (float(self.tool_data["CUTTER_DIAM"]) - self.get_tool_point_diameter()) / 2
        real_fl_len = self.clear_str_from_trailing_zeros(str(real_fl_len), sep=".").replace(".", "-")
        d = self.clear_str_from_trailing_zeros(str(self.tool_data["CUTTER_DIAM"]), sep=".").replace(".", "-")

        # l1 = self.clear_str_from_trailing_zeros(str(self.tool_data["FLUTE_LENGTH"]), sep=".").replace(".", "-")
        l2 = self.clear_str_from_trailing_zeros(str(self.tool_data["LENGTH"]), sep=".").replace(".", "-")

        t_name = (
            f"{self.file_name_prefix.upper()}"
            f"D{d}"
            f"_L{real_fl_len}"
            f"_L{l2}"
            # f"{self.file_name_suffix.upper()}"
        )
        return t_name


    @staticmethod
    def get_tool_point_angle() -> int:
        return 90

    def get_tool_point_diameter(self) -> int:
        return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["point_diameter"]

    @staticmethod
    def clear_str_from_trailing_zeros(str_to_clean: str, sep: str):
        new_str = str_to_clean.split(sep=sep)[0]
        try:
            rev_str_pt2 = str_to_clean.split(".")[1][::-1]
            rev_new_pt = ""
            for ch_i, char in enumerate(rev_str_pt2):
                if char != "0":
                    rev_new_pt += char
                else:
                    continue
            if rev_new_pt:
                new_str += sep + rev_new_pt[::-1]
            else:
                new_str += sep + "0"

        except:
            pass
        return new_str

    def calc_len_out_of_holder(self):
        return self.catalog_tool_geometry[self.create_tool_name_for_geom_catalogue()]["full_body_len"] / 2


    def calc_feed_rate(self, key_iso_material, RPM, fin_or_rough) -> float:
        try:
            Fn = self.catalog_cut_data[key_iso_material][config.key_fn][self.tool_data["cut_data_diam_group"]]
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            Fn = Fn * RPM * feed_multiplier
            return round(Fn, ndigits=config.NDIGITS_FEED)
        except:
            # logger.critical(f"{self.tool_data["tool_name_str"]} - feed per min not calculated")
            return 0

    def calc_feed_per_unit(self, key_iso_material, fin_or_rough: str) -> float:
        try:
            feed_multiplier = self.finishing_roughing_options[fin_or_rough]["feed_rate_multiplier"]
            Fn = self.catalog_cut_data[key_iso_material][config.key_fn][self.tool_data["cut_data_diam_group"]]
            # RPM = self.tool_data["cut_data"][key_iso_material][fin_or_rough]["TOOL_SPINDLE_RPM"]
            Fn = Fn * feed_multiplier
            return round(Fn, ndigits=config.NDIGITS_FEED_PER_UNIT)
        except:
            # logger.critical(f"{self.tool_data["tool_name_str"]} - feed per unit not calculated")
            return 0

    def calc_radial_depth(self, key_iso_material):
        return 0


    def set_xml_body_tool_params(self) -> str:
        xml_part_str = f"""\
    <ToolingSetup>
        <Tool Id="{self.tool_data["tool_name_for_xml"]}" RefXmlId="encref_1" Type="{self.tool_data["tool_type"]}">
            <Attr DataType="boolean" Name="UseOutline" Value="false"/>
            <Attr DataType="boolean" Name="ProLibraryTool" Value="false"/>
            <Attr DataType="boolean" Name="SketchTool" Value="false"/>
            <Attr DataType="boolean" Name="ToolByRef" Value="false"/>
            
            <ModelInfo FamilyName="COUNTERSINK_ASM" InstanceName="COUNTERSINK_ASM{self.d_for_bom()}" Type="Assembly"/>
            
            <MfgParam Name="CUTTER_DIAM" Value="{self.tool_data["CUTTER_DIAM"]}"/>
            <MfgParam Name="POINT_DIAMETER" Value="{self.point_diameter}"/>
            <MfgParam Name="POINT_ANGLE" Value="{self.point_angle}"/>
            <MfgParam Name="GAUGE_OFFSET" Value="-"/>
            <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
            <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>
            
            <MfgParam Name="HOLDER_DIA" Value="{self.tool_data["HOLDER_DIA"]}"/>
            <MfgParam Name="HOLDER_LEN" Value="{self.tool_data["HOLDER_LEN"]}"/>            
            
            <MfgParam Name="TOOL_MATERIAL" Value="{self.tool_data["TOOL_MATERIAL"]}"/>
            <MfgParam Name="LENGTH_UNITS" Value="{self.tool_data["LENGTH_UNITS"]}"/>
            <MfgParam Name="TOOL_COMMENT" Value="{self.tool_data["TOOL_COMMENT"]}"/>
            
            <MfgParam Name="GAUGE_X_LENGTH" Value="{self.tool_data["GAUGE_X_LENGTH"]}"/>
            <MfgParam Name="GAUGE_Z_LENGTH" Value="{self.tool_data["GAUGE_Z_LENGTH"]}"/>
            <MfgParam Name="COMP_OVERSIZE" Value="{self.tool_data["COMP_OVERSIZE"]}"/>
            <MfgParam Name="TOOL_LONG_FLAG" Value="{self.tool_data["TOOL_LONG_FLAG"]}"/>
            <MfgParam Name="COOLANT_OPTION" Value="{self.tool_data["COOLANT_OPTION"]}"/>
            <MfgParam Name="COOLANT_PRESSURE" Value="{self.tool_data["COOLANT_PRESSURE"]}"/>
            <MfgParam Name="SPINDLE_SENSE" Value="{self.tool_data["SPINDLE_SENSE"]}"/>
    """
        logger.debug(f"{self.tool_size_from_geom_catalogue} - xml_tool_params generated...")
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
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_rev" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["roughing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
                <Technology>
                    <Condition>
                        <MfgParam Name="APPLICATION_TYPE" Value="FINISHING"/>
                    </Condition>
                    <MfgParam Name="TOOL_SPINDLE_RPM" Unit="rev_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SPINDLE_RPM"]}"/>
                    <MfgParam Name="TOOL_SURFACE_SPEED" Unit="m_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_SURFACE_SPEED"]}"/>
                    <MfgParam Name="TOOL_FEED_RATE" Unit="mm_per_min" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_RATE"]}"/>
                    <MfgParam Name="TOOL_FEED_PER_UNIT" Unit="mm_per_rev" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_FEED_PER_UNIT"]}"/>
                    <MfgParam Name="TOOL_AXIAL_DEPTH" Unit="mm" Value="{self.tool_data["cut_data"][mat_iso_name]["finishing"]["TOOL_AXIAL_DEPTH"]}"/>
                </Technology>
            </ToolCutData>
        """
            total_string += xml_part_str

        logger.debug(f"{self.tool_size_from_geom_catalogue} - xml_tool_cut_data generated...")
        return total_string


    def set_xml_bom_components(self) -> str:
        xml_part_str = f"""\
            <BOM>
                <BOMComponent Comments=" " Name="BT40_COLLET_CHUCK" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40-45_PULL_STUD" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="BT40_HOLDER{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="COUNTERSINK_TAIL{self.d_for_bom()}" Quantity="1" Type="HOLDER"/>
                <BOMComponent Comments=" " Name="COUNTERSINK_CUTTER{self.d_for_bom()}" Quantity="1" Type="GENERAL"/>
            </BOM>
"""
        logger.debug(f"{self.tool_data["tool_name_str"]} - xml_BOM_components generated...")
        return xml_part_str


class CounterSinkTurnMill(CounterSink):
    holder_prefix = "TM_X_"
    family_name = "TM_X_ZENK_ASM"
    instance_name = "TM_X_ZENK_ASM"
    holder_name = "AXIAL_KOROTKY_EWS_107605"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
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
                <MfgParam Name="POINT_DIAMETER" Value="{self.point_diameter}"/>
                <MfgParam Name="POINT_ANGLE" Value="{self.point_angle}"/>
                <MfgParam Name="GAUGE_OFFSET" Value="-"/>
                <MfgParam Name="FLUTE_LENGTH" Value="{self.tool_data["FLUTE_LENGTH"]}"/>
                <MfgParam Name="LENGTH" Value="{self.tool_data["len_out_of_holder"]}"/>

                <MfgParam Name="SCP_TO_TAP_LEN" Value="{self.length_taken_by_holder}"/>
                <MfgParam Name="SAFE_LENGTH" Value="{self.max_safe_length}"/>

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
        logger.debug(f"{self.tool_size_from_geom_catalogue} - xml_tool_params generated...")
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


class CounterSinkTurnMill_TM_X(CounterSinkTurnMill):
    """
    TM_X_
    AXIAL_KOROTKY_EWS_107605
    """

    holder_prefix = "TM_X_"
    family_name = "TM_X_ZENK"
    instance_name = "TM_X_ZENK"
    holder_name = "AXIAL_KOROTKY_EWS_107605"
    tail_name = "ZENK_TAIL"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]

    cutter_name = "ZENK_CUT"


class CounterSinkTurnMill_TM_X_L(CounterSinkTurnMill):
    """
    TM_X_L_
    AXIAL_EWS_234762
    """
    holder_prefix = "TM_X_L_"
    family_name = "TM_X_L_ZENK"
    instance_name = "TM_X_L_ZENK"
    holder_name = "AXIAL_EWS_234762"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class CounterSinkTurnMill_TM_Z_1(CounterSinkTurnMill):
    """
    TM_Z_1_
    RADIAL_1_EWS_195136
    """
    holder_prefix = "TM_Z_1_"
    family_name = "TM_Z_1_ZENK"
    instance_name = "TM_Z_1_ZENK"
    holder_name = "RADIAL_1_EWS_195136"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class CounterSinkTurnMill_TM_Z_2(CounterSinkTurnMill):
    """
    TM_Z_2_
    RADIAL_2_EWS_196914
    """
    holder_prefix = "TM_Z_2_"
    family_name = "TM_Z_2_ZENK"
    instance_name = "TM_Z_2_ZENK"
    holder_name = "RADIAL_2_EWS_196914"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class CounterSinkTurnMill_TM_Z_SUB(CounterSinkTurnMill):
    """
    TM_Z_SUB_
    RADIAL_2_EWS_196914
    """
    holder_prefix = "TM_Z_SUB_"
    family_name = "TM_Z_SUB_ZENK"
    instance_name = "TM_Z_SUB_ZENK"
    holder_name = "RADIAL_2_EWS_196914"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class CounterSinkTurnMill_T_Z_ER(CounterSinkTurnMill):
    """
    T_Z_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """
    holder_prefix = "T_Z_ER_"
    family_name = "T_Z_ER_ZENK"
    instance_name = "T_Z_ER_ZENK"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "ZENK_TAIL"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]

    cutter_name = "ZENK_CUT"

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


class CounterSinkTurnMill_T_Z_SUB_ER(CounterSinkTurnMill):
    """
    T_Z_SUB_ER_
    HOLDER_L85_S02361
    HOLDER_COLLETS
    """
    holder_prefix = "T_Z_SUB_ER_"
    family_name = "T_Z_SUB_ER_ZENK"
    instance_name = "T_Z_SUB_ER_ZENK"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "ZENK_TAIL"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]

    cutter_name = "ZENK_CUT"

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


class CounterSinkTurnMill_T_Z(CounterSinkTurnMill):
    """
    T_Z_
    HOLDER_L85_S02361
    """
    holder_prefix = "T_Z_"
    family_name = "T_Z_ZENK"
    instance_name = "T_Z_ZENK"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class CounterSinkTurnMill_T_Z_SUB(CounterSinkTurnMill):
    """
    T_Z_SUB_
    HOLDER_L85_S02361
    """
    holder_prefix = "T_Z_SUB_"
    family_name = "T_Z_SUB_ZENK"
    instance_name = "T_Z_SUB_ZENK"
    holder_name = "HOLDER_L85_S02361"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
    max_safe_length = turnmill_holders_safe_lengths[holder_prefix]["max_safe_length"]
    length_taken_by_holder = turnmill_holders_safe_lengths[holder_prefix]["length_taken_by_holder"]


class CounterSinkTurnMill_T_Z_F2(CounterSinkTurnMill):
    """
    T_Z_F2_
    HOLDER_AXIS_EWS_135834
    """
    holder_prefix = "T_Z_F2_"
    family_name = "T_Z_F2_ZENK"
    instance_name = "T_Z_F2_ZENK"
    holder_name = "HOLDER_AXIS_EWS_135834"
    tail_name = "ZENK_TAIL"
    cutter_name = "ZENK_CUT"
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