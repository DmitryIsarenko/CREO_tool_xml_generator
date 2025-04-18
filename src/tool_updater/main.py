import logging

from src.tool_updater.classes.tool_classes.base_tool import BaseTool
from src.tool_updater.classes.tool_classes.axial.centerdrill import CenterDrill
from src.tool_updater.classes.tool_classes.axial.counterbore import CounterBore
from src.tool_updater.classes.tool_classes.axial.drill import Drill
from src.tool_updater.classes.tool_classes.axial.countersink import CounterSink
from src.tool_updater.classes.tool_classes.axial.reamer import Reamer
from src.tool_updater.classes.tool_classes.axial.tap import Tap
from src.tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferMill
from src.tool_updater.classes.tool_classes.milling.disk_mill import DiskOtreznoiFlat
from src.tool_updater.classes.tool_classes.milling.endmill import EndMill
from src.tool_updater.classes.tool_classes.milling.grib_mill import GribMillFlat
from src.tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from src.tool_updater.classes.tool_classes.milling.threadmill import ThreadMill
from src.tool_updater.classes.tool_classes.milling.toroid_mill import ToroidMill
from src.tool_updater.classes.tool_classes.milling.vnutr_rad_mill import VnutrRadMill
from src.tool_updater.classes.tool_generator import ToolGenerator
from tool_updater.classes.tool_classes.axial.tap import TapBlind, TapThrough
from tool_updater.classes.tool_classes.milling.disk_mill import DiskOtreznoiChamfer, DiskOtreznoiRounding
from tool_updater.classes.tool_classes.milling.grib_mill import GribMillRounding, GribMillChamfer
from tool_updater.classes.tool_classes.milling.index_mill import IndexMill, IndexMillSingleASMs

from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_TM_X
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_TM_X_L
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_T_Z
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.axial.drill import DrillTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.endmill import KontsTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.sphere_mill import SferaTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.toroid_mill import ToroidTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.chamfer_mill import ChamferTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_FlTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_ChTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.grib_mill import Grib_RoTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_ChTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_RoTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.disk_mill import Disk_FlTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.vnutr_rad_mill import R_VnutrTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_TM_X
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_TM_X_L
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_T_Z
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.milling.threadmill import ThreadTurnMill_T_Z_F2


from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_TM_X
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_TM_X_L
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_T_Z
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.axial.centerdrill import CenterDrillTurnMill_T_Z_F2


from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_TM_X
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_TM_X_L
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_T_Z
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.axial.countersink import CounterSinkTurnMill_T_Z_F2


from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_TM_X
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_TM_X_L
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_T_Z
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.axial.counterbore import CounterBoreTurnMill_T_Z_F2


from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_TM_X
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_TM_X_L
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_T_Z
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.axial.reamer import ReamerTurnMill_T_Z_F2


from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_TM_X
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_TM_X_L
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_T_Z
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.axial.tap import TapBlindTurnMill_T_Z_F2

from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_TM_X
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_TM_X_L
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_TM_Z_1
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_TM_Z_2
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_TM_Z_SUB
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_T_Z_ER
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_T_Z_SUB_ER
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_T_Z
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_T_Z_SUB
from tool_updater.classes.tool_classes.axial.tap import TapThroughTurnMill_T_Z_F2


logger = logging.getLogger("src")


# logger = logging.getLogger(__name__)

def gen_drills():
    ToolGenerator.create_tools(
        tool_class=Drill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Drill\Osawa 2386STI",
        debug_mode=0,

        teeth_num=1,
        file_name_prefix="sv_",
        file_name_suffix="_2386STI",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_regular_drills\2386STI.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_regular_drills\2386STI_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=Drill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Drill\Osawa 1692LS",
        debug_mode=0,

        teeth_num=1,
        file_name_prefix="sv_udlin_",
        file_name_suffix="_1692LS",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_extended_drills\1692LS.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_extended_drills\1692LS_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=Drill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Drill\China Extended",
        debug_mode=0,

        teeth_num=1,
        file_name_prefix="sv_udlin_",
        file_name_suffix="_China",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\China\1 geom.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\China\2 cut_data.json",
    )


def gen_turn_mill_drills():
    all_holders = {
        "TM_X": {
            "tool_class": DrillTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": DrillTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": DrillTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": DrillTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": DrillTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": DrillTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": DrillTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": DrillTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": DrillTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": DrillTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Drill\Osawa 2386STI",
            debug_mode=0,

            teeth_num=1,
            file_name_prefix=tool_prefix + "sv_",
            file_name_suffix="_2386STI",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_regular_drills\2386STI.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_regular_drills\2386STI_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Drill\Osawa 1692LS",
            debug_mode=0,

            teeth_num=1,
            file_name_prefix=tool_prefix + "sv_udlin_",
            file_name_suffix="_1692LS",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_extended_drills\1692LS.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\Osawa\hss_extended_drills\1692LS_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Drill\China Extended",
            debug_mode=0,

            teeth_num=1,
            file_name_prefix=tool_prefix + "sv_udlin_",
            file_name_suffix="_China",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\China\1 geom.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\drills\China\2 cut_data.json",
        )


def gen_endmills():
    ToolGenerator.create_tools(
        tool_class=EndMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\EndMill\Gesac UA100-S2",
        debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        file_name_prefix="fr_univ_",
        # file_name_prefix="fr_chern_",
        # file_name_prefix="fr_chist_",

        teeth_num=2,
        file_name_suffix="_UA100-S2",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling/endmills\Gesac\univ_isoN\UA100-S2\UA100-S2.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling/endmills\Gesac\univ_isoN\UA100-S2\UA100-S2_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=EndMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\EndMill\Gesac UA100-S3",
        debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        file_name_prefix="fr_univ_",
        # file_name_prefix="fr_chern_",
        # file_name_prefix="fr_chist_",

        teeth_num=3,
        file_name_suffix="_UA100-S3",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=EndMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\EndMill\Gesac UH360-S4",
        debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        file_name_prefix="fr_univ_",
        # file_name_prefix="fr_chern_",
        # file_name_prefix="fr_chist_",

        teeth_num=4,
        file_name_suffix="_UH360-S4",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4).json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4)_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=EndMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\EndMill\Gesac STR340-S4",
        debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        # file_name_prefix="fr_univ_",
        file_name_prefix="fr_chern_",
        # file_name_prefix="fr_chist_",

        teeth_num=4,
        file_name_suffix="_STR340-S4",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4).json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4)_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=EndMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\EndMill\Gesac UA100-SL3",
        debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        file_name_prefix="fr_konts_udlin_",

        teeth_num=3,
        file_name_suffix="_UA100-SL3",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=EndMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\EndMill\Gesac UP210-SL4",
        debug_mode=0,
        # debug_mode=1,
        # debug_mode=2,

        file_name_prefix="fr_konts_udlin_",

        teeth_num=4,
        file_name_suffix="_UP210-SL4",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4).json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4)_cut_data.json",
    )


def gen_turn_mill_endmills():
    all_holders = {
        "TM_X": {
            "tool_class": KontsTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": KontsTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": KontsTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": KontsTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": KontsTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": KontsTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": KontsTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": KontsTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": KontsTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": KontsTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\EndMill\Gesac UA100-S2",
            debug_mode=0,
            # debug_mode=1,
            # debug_mode=2,

            file_name_prefix=tool_prefix + "fr_univ_",
            # file_name_prefix="fr_chern_",
            # file_name_prefix="fr_chist_",

            teeth_num=2,
            file_name_suffix="_UA100-S2",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling/endmills\Gesac\univ_isoN\UA100-S2\UA100-S2.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling/endmills\Gesac\univ_isoN\UA100-S2\UA100-S2_cut_data.json",
        )

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\EndMill\Gesac UA100-S3",
            debug_mode=0,
            # debug_mode=1,
            # debug_mode=2,

            file_name_prefix=tool_prefix + "fr_univ_",
            # file_name_prefix="fr_chern_",
            # file_name_prefix="fr_chist_",

            teeth_num=3,
            file_name_suffix="_UA100-S3",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-S3\UA100-S3_cut_data.json",

        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\EndMill\Gesac UH360-S4",
            debug_mode=0,
            # debug_mode=1,
            # debug_mode=2,

            file_name_prefix=tool_prefix + "fr_univ_",
            # file_name_prefix="fr_chern_",
            # file_name_prefix="fr_chist_",

            teeth_num=4,
            file_name_suffix="_UH360-S4",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4).json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-S4(UH360-S4)\SS600-S4(UH360-S4)_cut_data.json",

        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\EndMill\Gesac STR340-S4",
            debug_mode=0,
            # debug_mode=1,
            # debug_mode=2,

            # file_name_prefix="fr_univ_",
            file_name_prefix=tool_prefix + "fr_chern_",
            # file_name_prefix="fr_chist_",

            teeth_num=4,
            file_name_suffix="_STR340-S4",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4).json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\rough_isoP_isoM\UPR210-S4(STR340-S4)\UPR210-S4(STR340-S4)_cut_data.json",

        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\EndMill\Gesac UA100-SL3",
            debug_mode=0,
            # debug_mode=1,
            # debug_mode=2,

            file_name_prefix=tool_prefix + "fr_konts_udlin_",

            teeth_num=3,
            file_name_suffix="_UA100-SL3",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoN\UA100-SL3\UA100-SL3_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\EndMill\Gesac UP210-SL4",
            debug_mode=0,
            # debug_mode=1,
            # debug_mode=2,

            file_name_prefix=tool_prefix + "fr_konts_udlin_",

            teeth_num=4,
            file_name_suffix="_UP210-SL4",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4).json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\endmills\Gesac\univ_isoP_iso_M\SS600-SL4(UP210-SL4)\SS600-SL4(UP210-SL4)_cut_data.json",
        )


def gen_ballmills():
    ToolGenerator.create_tools(
        tool_class=BallMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\BallMill\Gesac UA100-B2",
        debug_mode=0,

        file_name_prefix="sfera_",
        # file_name_prefix="sfera_chist_",
        # file_name_prefix="sfera_chern_",

        teeth_num=2,
        file_name_suffix="_UA100-B2",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\UA100-B2\UA100-B2.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\UA100-B2\UA100-B2_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=BallMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\BallMill\Gesac SS600-B4",
        debug_mode=0,

        file_name_prefix="sfera_",
        # file_name_prefix="sfera_chist_",
        # file_name_prefix="sfera_chern_",

        teeth_num=4,
        file_name_suffix="_SS600-B4",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\SS600-B4/SS600-B4.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\SS600-B4/SS600-B4_cut_data.json",
    )


def gen_turn_mill_ballmills():
    all_holders = {
        "TM_X": {
            "tool_class": SferaTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": SferaTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": SferaTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": SferaTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": SferaTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": SferaTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": SferaTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": SferaTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": SferaTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": SferaTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\BallMill\Gesac UA100-B2",
            debug_mode=0,

            file_name_prefix=tool_prefix + "sfera_",

            teeth_num=2,
            file_name_suffix="_UA100-B2",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\UA100-B2\UA100-B2.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\UA100-B2\UA100-B2_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\BallMill\Gesac SS600-B4",
            debug_mode=0,

            file_name_prefix=tool_prefix + "sfera_",
            teeth_num=4,
            file_name_suffix="_SS600-B4",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\SS600-B4/SS600-B4.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\ballnose_mills\Gesac\SS600-B4/SS600-B4_cut_data.json",
        )


def gen_toroidmills():
    ToolGenerator.create_tools(
        tool_class=ToroidMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ToroidMill\Gesac UA100-R3",
        debug_mode=0,

        file_name_prefix="fr_tor_",
        # file_name_prefix="fr_tor_chist_",
        # file_name_prefix="fr_tor_chern_",

        teeth_num=3,
        file_name_suffix="_UA100-R3",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoN\UA100-R3\UA100-R3.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoN\UA100-R3\UA100-R3_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=ToroidMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ToroidMill\Gesac SS600-R4",
        debug_mode=0,

        file_name_prefix="fr_tor_",
        # file_name_prefix="fr_tor_chist_",
        # file_name_prefix="fr_tor_chern_",

        teeth_num=4,
        file_name_suffix="_SS600-R4",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoP_isoM\SS600-R4\SS600-R4.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoP_isoM\SS600-R4\SS600-R4_cut_data.json",
    )


def gen_turn_mill_toroidmills():
    all_holders = {
        "TM_X": {
            "tool_class": ToroidTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": ToroidTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": ToroidTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": ToroidTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": ToroidTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": ToroidTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": ToroidTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": ToroidTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": ToroidTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": ToroidTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ToroidMill\Gesac UA100-R3",
            debug_mode=0,

            file_name_prefix=tool_prefix + "fr_tor_",
            # file_name_prefix="fr_tor_chist_",
            # file_name_prefix="fr_tor_chern_",

            teeth_num=3,
            file_name_suffix="_UA100-R3",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoN\UA100-R3\UA100-R3.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoN\UA100-R3\UA100-R3_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ToroidMill\Gesac SS600-R4",
            debug_mode=0,

            file_name_prefix=tool_prefix + "fr_tor_",
            # file_name_prefix="fr_tor_chist_",
            # file_name_prefix="fr_tor_chern_",

            teeth_num=4,
            file_name_suffix="_SS600-R4",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoP_isoM\SS600-R4\SS600-R4.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\toroidal_endmills\Gesac\isoP_isoM\SS600-R4\SS600-R4_cut_data.json",
        )


def gen_disk_mills():
    ToolGenerator.create_tools(
        tool_class=DiskOtreznoiFlat,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\DiskOtreznoi\Iscar SGSF-GSFN",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="disk_",
        file_name_suffix="_SGSF_GSFN",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\otrez_disk\Iscar GSFN\SGSF_GSFN.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\otrez_disk\Iscar GSFN\SGSF_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=DiskOtreznoiChamfer,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\DiskOtreznoi\Iscar SGSF-E8 GSFP-5.4-90",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="disk_",
        file_name_suffix="_SGSF_GSFP",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar E8 GSFP-5.4-90\SGSF_GSFP.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar E8 GSFP-5.4-90\SGSF_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=DiskOtreznoiRounding,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\DiskOtreznoi\Iscar SGSF-GSFU",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="disk_",
        file_name_suffix="_SGSF_GSFU",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar GSFU\SGSF_GSFU.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar GSFU\SGSF_cut_data.json",
    )


def gen_turn_mill_disks():
    gen_turn_mill_disks_flat()
    gen_turn_mill_disks_chamfer()
    gen_turn_mill_disks_rounding()


def gen_turn_mill_disks_chamfer():
    all_holders = {
        "TM_X": {
            "tool_class": Disk_ChTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": Disk_ChTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": Disk_ChTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": Disk_ChTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": Disk_ChTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": Disk_ChTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": Disk_ChTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": Disk_ChTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": Disk_ChTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": Disk_ChTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            #             tool_class=DiskOtreznoiChamfer,
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\DiskOtreznoi\Iscar SGSF-E8 GSFP-5.4-90",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "disk_",
            file_name_suffix="_SGSF_GSFP",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar E8 GSFP-5.4-90\SGSF_GSFP.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar E8 GSFP-5.4-90\SGSF_cut_data.json",
        )


def gen_turn_mill_disks_rounding():
    all_holders = {
        "TM_X": {
            "tool_class": Disk_RoTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": Disk_RoTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": Disk_RoTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": Disk_RoTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": Disk_RoTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": Disk_RoTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": Disk_RoTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": Disk_RoTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": Disk_RoTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": Disk_RoTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            #             tool_class=DiskOtreznoiRounding,
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\DiskOtreznoi\Iscar SGSF-GSFU",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "disk_",
            file_name_suffix="_SGSF_GSFU",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar GSFU\SGSF_GSFU.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/otrez_disk/Iscar GSFU\SGSF_cut_data.json",
        )


def gen_turn_mill_disks_flat():
    all_holders = {
        "TM_X": {
            "tool_class": Disk_FlTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": Disk_FlTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": Disk_FlTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": Disk_FlTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": Disk_FlTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": Disk_FlTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": Disk_FlTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": Disk_FlTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": Disk_FlTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": Disk_FlTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            # tool_class=DiskOtreznoiFlat,
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\DiskOtreznoi\Iscar SGSF-GSFN",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "disk_",
            file_name_suffix="_SGSF_GSFN",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\otrez_disk\Iscar GSFN\SGSF_GSFN.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\otrez_disk\Iscar GSFN\SGSF_cut_data.json",
        )


def gen_zenkovki():
    ToolGenerator.create_tools(
        tool_class=CounterSink,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\CounterSink\Precitool 110120",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="zenk_",
        file_name_suffix="_110120",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\countersinks\Precitool\110120\110120.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\countersinks\Precitool\110120\110120_cut_data.json",
    )


def gen_centrovki():
    ToolGenerator.create_tools(
        tool_class=CenterDrill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\CenterDrill\Precitool 105200",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="centr_",
        file_name_suffix="_105200",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105200\105200.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105200\105200_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=CenterDrill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\CenterDrill\Precitool 105600L",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="centr_udlin_",
        file_name_suffix="_105600L",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105600L - extended\105600L.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105600L - extended\105600L_cut_data.json",
    )


def gen_metchiki():
    ToolGenerator.create_tools(
        tool_class=TapBlind,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Tap\Garant Metric Blind 135850",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="metchik_gluh_",
        file_name_suffix="_135850",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\blind_hole\135850\135850.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\blind_hole\135850\135850_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=TapThrough,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Tap\Garant Metric through 132640",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="metchik_skvozn_",
        file_name_suffix="_132640",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\through_hole\132640\132640.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\through_hole\132640\132640_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=TapBlind,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Tap\Garant Inch blind 137805",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="metchik_gluh_",
        file_name_suffix="_137805",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\blind_hole\137805\137805.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\blind_hole\137805\137805_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=TapThrough,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Tap\Garant Inch through 133300",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="metchik_skvozn_",
        file_name_suffix="_133300",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\through_hole\133300\133300.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\through_hole\133300\133300_cut_data.json",
    )

def gen_turnmill_metchiki():
    gen_turnmill_metchiki_blind()
    gen_turnmill_metchiki_through()

def gen_turnmill_metchiki_blind():
    all_holders = {
        "TM_X": {
            "tool_class": TapBlindTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": TapBlindTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": TapBlindTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": TapBlindTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": TapBlindTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": TapBlindTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": TapBlindTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": TapBlindTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": TapBlindTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": TapBlindTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"


        ToolGenerator.create_tools(
            # tool_class=TapBlind,
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Tap\Garant Metric Blind 135850",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "metchik_gluh_",
            file_name_suffix="_135850",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\blind_hole\135850\135850.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\blind_hole\135850\135850_cut_data.json",
        )

        ToolGenerator.create_tools(
#             tool_class=TapBlind,
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Tap\Garant Inch blind 137805",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "metchik_gluh_",
            file_name_suffix="_137805",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\blind_hole\137805\137805.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\blind_hole\137805\137805_cut_data.json",
        )



def gen_turnmill_metchiki_through():
    all_holders = {
        "TM_X": {
            "tool_class": TapBlindTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": TapBlindTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": TapBlindTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": TapBlindTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": TapBlindTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": TapBlindTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": TapBlindTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": TapBlindTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": TapBlindTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": TapBlindTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"


        ToolGenerator.create_tools(
            #             tool_class=TapThrough,
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Tap\Garant Metric through 132640",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "metchik_skvozn_",
            file_name_suffix="_132640",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\through_hole\132640\132640.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\metric\through_hole\132640\132640_cut_data.json",
        )

        ToolGenerator.create_tools(
            #             tool_class=TapThrough,
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Tap\Garant Inch through 133300",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "metchik_skvozn_",
            file_name_suffix="_133300",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\through_hole\133300\133300.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\taps\Garant\inch\through_hole\133300\133300_cut_data.json",
        )


def gen_vnutr_rad_mills():
    ToolGenerator.create_tools(
        tool_class=VnutrRadMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\VnutrRadMill\Precitool 178815",
        teeth_num=4,
        debug_mode=0,

        file_name_prefix="vnutr_rad_",
        file_name_suffix="_178815",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\internal_R\Precitool\178815\178815_cut_data.json",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\internal_R\Precitool\178815\178815.json",
    )

def gen_turn_mill_vnutr_rad_mills():
    all_holders = {
        "TM_X": {
            "tool_class": R_VnutrTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": R_VnutrTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": R_VnutrTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": R_VnutrTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": R_VnutrTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": R_VnutrTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": R_VnutrTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": R_VnutrTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": R_VnutrTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": R_VnutrTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\VnutrRadMill\Precitool 178815",
            teeth_num=4,
            debug_mode=0,

            file_name_prefix=tool_prefix + "vnutr_rad_",
            file_name_suffix="_178815",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\internal_R\Precitool\178815\178815_cut_data.json",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\internal_R\Precitool\178815\178815.json",
        )


def gen_razvertki():
    ToolGenerator.create_tools(
        tool_class=Reamer,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Reamer\Guhring 1409",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="razvert_",
        file_name_suffix="_1409",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1409\1409.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1409\1409_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=Reamer,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Reamer\Garant 162961",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="razvert_udlin_",
        file_name_suffix="_162961",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Garant\162961\162961.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Garant\162961\162961_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=Reamer,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\Reamer\Guhring 1411",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="razvert_",
        file_name_suffix="_1411",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1411\1411.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1411\1411_cut_data.json",
    )


def gen_cekovki():
    ToolGenerator.create_tools(
        tool_class=CounterBore,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\CounterBore\Precitool 111010",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="cekov_",
        file_name_suffix="_111010",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\counterbores\Precitool\111010\111010.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\counterbores\Precitool\111010\111010_cut_data.json",
    )


def gen_turn_mill_centrovki():
    all_holders = {
        "TM_X": {
            "tool_class": CenterDrillTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": CenterDrillTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": CenterDrillTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": CenterDrillTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": CenterDrillTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": CenterDrillTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": CenterDrillTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": CenterDrillTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": CenterDrillTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": CenterDrillTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\CenterDrill\Precitool 105200",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "centr_",
            file_name_suffix="_105200",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105200\105200.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105200\105200_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\CenterDrill\Precitool 105600L",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "centr_udlin_",
            file_name_suffix="_105600L",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105600L - extended\105600L.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\center_drills\Precitool\105600L - extended\105600L_cut_data.json",
        )


def gen_turn_mill_zenkovki():
    all_holders = {
        "TM_X": {
            "tool_class": CounterSinkTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": CounterSinkTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": CounterSinkTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": CounterSinkTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": CounterSinkTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": CounterSinkTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": CounterSinkTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": CounterSinkTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": CounterSinkTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": CounterSinkTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"


        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\CounterSink\Precitool 110120",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "zenk_",
            file_name_suffix="_110120",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\countersinks\Precitool\110120\110120.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\countersinks\Precitool\110120\110120_cut_data.json",
        )


def gen_turn_mill_cekovki():
    all_holders = {
        "TM_X": {
            "tool_class": CounterBoreTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": CounterBoreTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": CounterBoreTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": CounterBoreTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": CounterBoreTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": CounterBoreTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": CounterBoreTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": CounterBoreTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": CounterBoreTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": CounterBoreTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"


        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\CounterBore\Precitool 111010",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "cekov_",
            file_name_suffix="_111010",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\counterbores\Precitool\111010\111010.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\counterbores\Precitool\111010\111010_cut_data.json",
        )




def gen_turn_mill_razvertki():
    all_holders = {
        "TM_X": {
            "tool_class": ReamerTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": ReamerTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": ReamerTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": ReamerTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": ReamerTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": ReamerTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": ReamerTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": ReamerTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": ReamerTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": ReamerTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Reamer\Guhring 1409",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "razvert_",
            file_name_suffix="_1409",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1409\1409.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1409\1409_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Reamer\Garant 162961",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "razvert_udlin_",
            file_name_suffix="_162961",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Garant\162961\162961.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Garant\162961\162961_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\Reamer\Guhring 1411",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "razvert_",
            file_name_suffix="_1411",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1411\1411.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\axial\reamers\Guhring\1411\1411_cut_data.json",
        )


def gen_ugloviye():
    ToolGenerator.create_tools(
        tool_class=ChamferMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ChamferMill\Gesac UP210-L60",
        teeth_num=4,
        debug_mode=0,

        file_name_prefix="uglovaya_",
        file_name_suffix="_UP210-L60",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L60.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L60_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=ChamferMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ChamferMill\Gesac UP210-L90",
        teeth_num=4,
        debug_mode=0,

        file_name_prefix="uglovaya_",
        file_name_suffix="_UP210-L90",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L90.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L90_cut_data.json",
    )
    ToolGenerator.create_tools(
        tool_class=ChamferMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ChamferMill\Gesac UP210-L120",
        teeth_num=4,
        debug_mode=0,

        file_name_prefix="uglovaya_",
        file_name_suffix="_UP210-L120",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L120.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L120_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=ChamferMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ChamferMill\Special A30",
        teeth_num=4,
        debug_mode=0,

        file_name_prefix="uglovaya_",
        file_name_suffix="_A30",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L30.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L30_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=ChamferMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ChamferMill\Special A45",
        teeth_num=4,
        debug_mode=0,

        file_name_prefix="uglovaya_",
        file_name_suffix="_A45",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L45.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L45_cut_data.json",
    )


def gen_turn_mill_ugloviye():
    all_holders = {
        "TM_X": {
            "tool_class": ChamferTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": ChamferTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": ChamferTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": ChamferTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": ChamferTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": ChamferTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": ChamferTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": ChamferTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": ChamferTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": ChamferTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ChamferMill\Gesac UP210-L60",
            teeth_num=4,
            debug_mode=0,

            file_name_prefix=tool_prefix + "uglovaya_",
            file_name_suffix="_UP210-L60",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L60.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L60_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ChamferMill\Gesac UP210-L90",
            teeth_num=4,
            debug_mode=0,

            file_name_prefix=tool_prefix + "uglovaya_",
            file_name_suffix="_UP210-L90",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L90.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L90_cut_data.json",
        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ChamferMill\Gesac UP210-L120",
            teeth_num=4,
            debug_mode=0,

            file_name_prefix=tool_prefix + "uglovaya_",
            file_name_suffix="_UP210-L120",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L120.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\Gesac\UP210\UP210-L120_cut_data.json",
        )

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ChamferMill\Special A30",
            teeth_num=4,
            debug_mode=0,

            file_name_prefix=tool_prefix + "uglovaya_",
            file_name_suffix="_A30",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L30.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L30_cut_data.json",
        )

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ChamferMill\Special A45",
            teeth_num=4,
            debug_mode=0,

            file_name_prefix=tool_prefix + "uglovaya_",
            file_name_suffix="_A45",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L45.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\chamfer_mills\special\L45_cut_data.json",
        )


def gen_gribkovie():
    ToolGenerator.create_tools(
        tool_class=GribMillRounding,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\GribMill\Iscar MM GRIT",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="grib_",
        file_name_suffix="_GRIT",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT\GRIT.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT\GRIT_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=GribMillChamfer,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\GribMill\Iscar MM GRIT-45A",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="grib_",
        file_name_suffix="_GRIT-45A",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT-45A\GRIT-45A.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT\GRIT_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=GribMillRounding,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\GribMill\Iscar MM TS-H",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="grib_",
        file_name_suffix="_TS-H",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\TS-H\TS-H.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\TS-H\TS-H_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=GribMillRounding,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\GribMill\Iscar MM TS-N rounding",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="grib_",
        file_name_suffix="_TS-N",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N rounding\TS-N.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N rounding\TS-N_cut_data.json",
    )

    ToolGenerator.create_tools(
        tool_class=GribMillChamfer,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\GribMill\Iscar MM TS-N chamfer",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="grib_",
        file_name_suffix="_TS-N",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N chamfer\TS-N.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N chamfer\TS-N_cut_data.json",
    )


def gen_turn_mill_gribkovie():
    gen_turn_mill_gribkovie_flat()
    gen_turn_mill_gribkovie_chamfer()
    gen_turn_mill_gribkovie_rounding()


def gen_turn_mill_gribkovie_chamfer():
    all_holders = {
        "TM_X": {
            "tool_class": Grib_ChTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": Grib_ChTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": Grib_ChTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": Grib_ChTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": Grib_ChTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": Grib_ChTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": Grib_ChTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": Grib_ChTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": Grib_ChTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": Grib_ChTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\GribMill\Iscar MM GRIT-45A",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "grib_",
            file_name_suffix="_GRIT-45A",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT-45A\GRIT-45A.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT\GRIT_cut_data.json",
        )

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\GribMill\Iscar MM TS-N chamfer",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "grib_",
            file_name_suffix="_TS-N",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N chamfer\TS-N.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N chamfer\TS-N_cut_data.json",
        )


def gen_turn_mill_gribkovie_rounding():
    all_holders = {
        "TM_X": {
            "tool_class": Grib_RoTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": Grib_RoTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": Grib_RoTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": Grib_RoTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": Grib_RoTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": Grib_RoTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": Grib_RoTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": Grib_RoTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": Grib_RoTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": Grib_RoTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\GribMill\Iscar MM GRIT",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "grib_",
            file_name_suffix="_GRIT",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT\GRIT.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\GRIT\GRIT_cut_data.json",
        )

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\GribMill\Iscar MM TS-H",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "grib_",
            file_name_suffix="_TS-H",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\TS-H\TS-H.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\gribkovie\Iscar\MultiMaster\TS-H\TS-H_cut_data.json",
        )

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\GribMill\Iscar MM TS-N rounding",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "grib_",
            file_name_suffix="_TS-N",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N rounding\TS-N.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src/tool_updater/catalogs/milling/gribkovie/Iscar/MultiMaster/TS-N rounding\TS-N_cut_data.json",
        )


def gen_turn_mill_gribkovie_flat():
    all_holders = {
        "TM_X": {
            "tool_class": Grib_FlTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": Grib_FlTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": Grib_FlTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": Grib_FlTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": Grib_FlTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": Grib_FlTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": Grib_FlTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": Grib_FlTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": Grib_FlTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": Grib_FlTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]
        tool_prefix = holder_subdir.lower() + "_"

        pass


def gen_rezbofrezi():
    ToolGenerator.create_tools(
        tool_class=ThreadMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ThreadMill\Vardex Metric Helicool",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="rezbofr_",
        file_name_suffix="_helicool",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\metric\helicool_m.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\metric\helicool_m_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=ThreadMill,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\ThreadMill\Vardex Inch Helicool",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="rezbofr_",
        file_name_suffix="_helicool",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\inch\helicool_g.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\inch\helicool_g_cut_data.json",
    )

def gen_turn_mill_rezbofrezi():
    all_holders = {
        "TM_X": {
            "tool_class": ThreadTurnMill_TM_X,
            "holder_subdir": "TM_X"
        },
        "TM_X_L": {
            "tool_class": ThreadTurnMill_TM_X_L,
            "holder_subdir": "TM_X_L"
        },
        "TM_Z_1": {
            "tool_class": ThreadTurnMill_TM_Z_1,
            "holder_subdir": "TM_Z_1"
        },
        "TM_Z_2": {
            "tool_class": ThreadTurnMill_TM_Z_2,
            "holder_subdir": "TM_Z_2"
        },
        "TM_Z_SUB": {
            "tool_class": ThreadTurnMill_TM_Z_SUB,
            "holder_subdir": "TM_Z_SUB"
        },
        "T_Z_ER": {
            "tool_class": ThreadTurnMill_T_Z_ER,
            "holder_subdir": "T_Z_ER"
        },
        "T_Z_SUB_ER": {
            "tool_class": ThreadTurnMill_T_Z_SUB_ER,
            "holder_subdir": "T_Z_SUB_ER"
        },
        "T_Z": {
            "tool_class": ThreadTurnMill_T_Z,
            "holder_subdir": "T_Z"
        },
        "T_Z_SUB": {
            "tool_class": ThreadTurnMill_T_Z_SUB,
            "holder_subdir": "T_Z_SUB"
        },
        "T_Z_F2": {
            "tool_class": ThreadTurnMill_T_Z_F2,
            "holder_subdir": "T_Z_F2"
        },
    }

    for holder in all_holders:
        holder_subdir = all_holders[holder]["holder_subdir"]
        tool_class = all_holders[holder]["tool_class"]

        tool_prefix = holder_subdir.lower() + "_"

        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ThreadMill\Vardex Metric Helicool",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "rezbofr_",
            file_name_suffix="_helicool",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\metric\helicool_m.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\metric\helicool_m_cut_data.json",

        )
        ToolGenerator.create_tools(
            tool_class=tool_class,
            target_path=fr"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\TurnMill\{holder_subdir}\ThreadMill\Vardex Inch Helicool",
            teeth_num=1,
            debug_mode=0,

            file_name_prefix=tool_prefix + "rezbofr_",
            file_name_suffix="_helicool",
            path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\inch\helicool_g.json",
            path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\thread_milling\Vardex\Helicool\inch\helicool_g_cut_data.json",
        )



def gen_index_mills():
    ToolGenerator.create_tools(
        tool_class=IndexMillSingleASMs,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\IndexMill\Taegu Tec\3P TE90-10",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="",
        file_name_suffix=" Taegu Tec",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Taegu Tec\3P TE90-10\3_geom.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Taegu Tec\3P TE90-10\4_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=IndexMillSingleASMs,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\IndexMill\Taegu Tec\3P TE90-15",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="",
        file_name_suffix=" Taegu Tec",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Taegu Tec\3P TE90-15\3_geom.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Taegu Tec\3P TE90-15\4_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=IndexMillSingleASMs,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\IndexMill\Taegu Tec\3P TF90-15",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="",
        file_name_suffix=" Taegu Tec",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Taegu Tec\3P TF90-15\3_geom.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Taegu Tec\3P TF90-15\4_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=IndexMillSingleASMs,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\IndexMill\Mitsubishi\AJX",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="",
        file_name_suffix=" Mitsubishi",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Mitsubishi\AJX\3_geom.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Mitsubishi\AJX\4_cut_data.json",

    )
    ToolGenerator.create_tools(
        tool_class=IndexMillSingleASMs,
        target_path=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\база инструмента\target_path\IndexMill\Mitsubishi\APX3000",
        teeth_num=1,
        debug_mode=0,

        file_name_prefix="",
        file_name_suffix=" Mitsubishi",
        path_to_catalog_geometry=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Mitsubishi\APX3000\3_geom.json",
        path_to_catalog_cut_data=r"c:\WORK_DIRECTORY\10_Programming\Projects\tool_base\tool_base\src\tool_updater\catalogs\milling\index_mills\Mitsubishi\APX3000\4_cut_data.json",

    )


def main():
    # VHMs
    # gen_endmills()
    # gen_toroidmills()
    # gen_ballmills()

    # chamfers and rad
    # gen_ugloviye()
    # gen_vnutr_rad_mills()

    # threads
    # gen_rezbofrezi()
    # gen_metchiki()

    # index mills
    # gen_disk_mills()
    # gen_gribkovie()
    # gen_index_mills()

    # axial
    # gen_centrovki()
    # gen_drills()
    # gen_zenkovki()
    # gen_cekovki()
    # gen_razvertki()


    # turnmill
    #   axial
    # gen_turn_mill_drills()
    # gen_turn_mill_centrovki()
    # gen_turn_mill_zenkovki()
    # gen_turn_mill_cekovki()
    # gen_turn_mill_razvertki()


    #   milling
    # gen_turn_mill_endmills()
    # gen_turn_mill_ballmills()
    # gen_turn_mill_toroidmills()

    #   chamfers and rad
    # gen_turn_mill_ugloviye()
    # gen_turn_mill_vnutr_rad_mills()

    #   index mills
    # gen_turn_mill_gribkovie()
    # gen_turn_mill_disks()
    # gen_turn_mill_index_mills()


    # threads
    # gen_turn_mill_rezbofrezi()
    # gen_turnmill_metchiki()


    """
    freza_konts_
    freza_konts_udlin_
    freza_konts_strujkolom_
    freza_toroid_
    freza_sfera_
    freza_sfera_udlin_
    freza_uglov_
    freza_otrez_disk_
    freza_grib_
    freza_vnutr_rad_
    rezbofr_metrich_
    rezbofr_trubn_
    centrovka_
    sverlo_
    sverlo_udlin_
    zenkovka_
    cekovka_
    metchik_m..
    metchik_g..
    razvertka_
    blok_rastoch_
    """

    pass


if __name__ == '__main__':
    main()
