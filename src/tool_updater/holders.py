"""Holder class mappings shared by catalog job builders."""

from src.tool_updater.classes.tool_classes.axial.centerdrill import (
    CenterDrillTurnMill_T_Z,
    CenterDrillTurnMill_T_Z_ER,
    CenterDrillTurnMill_T_Z_F2,
    CenterDrillTurnMill_T_Z_SUB,
    CenterDrillTurnMill_T_Z_SUB_ER,
    CenterDrillTurnMill_TM_X,
    CenterDrillTurnMill_TM_X_L,
    CenterDrillTurnMill_TM_Z_1,
    CenterDrillTurnMill_TM_Z_2,
    CenterDrillTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.axial.counterbore import (
    CounterBoreTurnMill_T_Z,
    CounterBoreTurnMill_T_Z_ER,
    CounterBoreTurnMill_T_Z_F2,
    CounterBoreTurnMill_T_Z_SUB,
    CounterBoreTurnMill_T_Z_SUB_ER,
    CounterBoreTurnMill_TM_X,
    CounterBoreTurnMill_TM_X_L,
    CounterBoreTurnMill_TM_Z_1,
    CounterBoreTurnMill_TM_Z_2,
    CounterBoreTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.axial.countersink import (
    CounterSinkTurnMill_T_Z,
    CounterSinkTurnMill_T_Z_ER,
    CounterSinkTurnMill_T_Z_F2,
    CounterSinkTurnMill_T_Z_SUB,
    CounterSinkTurnMill_T_Z_SUB_ER,
    CounterSinkTurnMill_TM_X,
    CounterSinkTurnMill_TM_X_L,
    CounterSinkTurnMill_TM_Z_1,
    CounterSinkTurnMill_TM_Z_2,
    CounterSinkTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.axial.drill import (
    DrillTurnMill_T_Z,
    DrillTurnMill_T_Z_ER,
    DrillTurnMill_T_Z_F2,
    DrillTurnMill_T_Z_SUB,
    DrillTurnMill_T_Z_SUB_ER,
    DrillTurnMill_TM_X,
    DrillTurnMill_TM_X_L,
    DrillTurnMill_TM_Z_1,
    DrillTurnMill_TM_Z_2,
    DrillTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.axial.reamer import (
    ReamerTurnMill_T_Z,
    ReamerTurnMill_T_Z_ER,
    ReamerTurnMill_T_Z_F2,
    ReamerTurnMill_T_Z_SUB,
    ReamerTurnMill_T_Z_SUB_ER,
    ReamerTurnMill_TM_X,
    ReamerTurnMill_TM_X_L,
    ReamerTurnMill_TM_Z_1,
    ReamerTurnMill_TM_Z_2,
    ReamerTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.axial.tap import (
    TapBlindTurnMill_T_Z,
    TapBlindTurnMill_T_Z_ER,
    TapBlindTurnMill_T_Z_F2,
    TapBlindTurnMill_T_Z_SUB,
    TapBlindTurnMill_T_Z_SUB_ER,
    TapBlindTurnMill_TM_X,
    TapBlindTurnMill_TM_X_L,
    TapBlindTurnMill_TM_Z_1,
    TapBlindTurnMill_TM_Z_2,
    TapBlindTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.chamfer_mill import (
    ChamferTurnMill_T_Z,
    ChamferTurnMill_T_Z_ER,
    ChamferTurnMill_T_Z_F2,
    ChamferTurnMill_T_Z_SUB,
    ChamferTurnMill_T_Z_SUB_ER,
    ChamferTurnMill_TM_X,
    ChamferTurnMill_TM_X_L,
    ChamferTurnMill_TM_Z_1,
    ChamferTurnMill_TM_Z_2,
    ChamferTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.disk_mill import (
    Disk_ChTurnMill_T_Z,
    Disk_ChTurnMill_T_Z_ER,
    Disk_ChTurnMill_T_Z_F2,
    Disk_ChTurnMill_T_Z_SUB,
    Disk_ChTurnMill_T_Z_SUB_ER,
    Disk_ChTurnMill_TM_X,
    Disk_ChTurnMill_TM_X_L,
    Disk_ChTurnMill_TM_Z_1,
    Disk_ChTurnMill_TM_Z_2,
    Disk_ChTurnMill_TM_Z_SUB,
    Disk_FlTurnMill_T_Z,
    Disk_FlTurnMill_T_Z_ER,
    Disk_FlTurnMill_T_Z_F2,
    Disk_FlTurnMill_T_Z_SUB,
    Disk_FlTurnMill_T_Z_SUB_ER,
    Disk_FlTurnMill_TM_X,
    Disk_FlTurnMill_TM_X_L,
    Disk_FlTurnMill_TM_Z_1,
    Disk_FlTurnMill_TM_Z_2,
    Disk_FlTurnMill_TM_Z_SUB,
    Disk_RoTurnMill_T_Z,
    Disk_RoTurnMill_T_Z_ER,
    Disk_RoTurnMill_T_Z_F2,
    Disk_RoTurnMill_T_Z_SUB,
    Disk_RoTurnMill_T_Z_SUB_ER,
    Disk_RoTurnMill_TM_X,
    Disk_RoTurnMill_TM_X_L,
    Disk_RoTurnMill_TM_Z_1,
    Disk_RoTurnMill_TM_Z_2,
    Disk_RoTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.endmill import (
    KontsTurnMill_T_Z,
    KontsTurnMill_T_Z_ER,
    KontsTurnMill_T_Z_F2,
    KontsTurnMill_T_Z_SUB,
    KontsTurnMill_T_Z_SUB_ER,
    KontsTurnMill_TM_X,
    KontsTurnMill_TM_X_L,
    KontsTurnMill_TM_Z_1,
    KontsTurnMill_TM_Z_2,
    KontsTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.grib_mill import (
    Grib_ChTurnMill_T_Z,
    Grib_ChTurnMill_T_Z_ER,
    Grib_ChTurnMill_T_Z_F2,
    Grib_ChTurnMill_T_Z_SUB,
    Grib_ChTurnMill_T_Z_SUB_ER,
    Grib_ChTurnMill_TM_X,
    Grib_ChTurnMill_TM_X_L,
    Grib_ChTurnMill_TM_Z_1,
    Grib_ChTurnMill_TM_Z_2,
    Grib_ChTurnMill_TM_Z_SUB,
    Grib_FlTurnMill_T_Z,
    Grib_FlTurnMill_T_Z_ER,
    Grib_FlTurnMill_T_Z_F2,
    Grib_FlTurnMill_T_Z_SUB,
    Grib_FlTurnMill_T_Z_SUB_ER,
    Grib_FlTurnMill_TM_X,
    Grib_FlTurnMill_TM_X_L,
    Grib_FlTurnMill_TM_Z_1,
    Grib_FlTurnMill_TM_Z_2,
    Grib_FlTurnMill_TM_Z_SUB,
    Grib_RoTurnMill_T_Z,
    Grib_RoTurnMill_T_Z_ER,
    Grib_RoTurnMill_T_Z_F2,
    Grib_RoTurnMill_T_Z_SUB,
    Grib_RoTurnMill_T_Z_SUB_ER,
    Grib_RoTurnMill_TM_X,
    Grib_RoTurnMill_TM_X_L,
    Grib_RoTurnMill_TM_Z_1,
    Grib_RoTurnMill_TM_Z_2,
    Grib_RoTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.sphere_mill import (
    SferaTurnMill_T_Z,
    SferaTurnMill_T_Z_ER,
    SferaTurnMill_T_Z_F2,
    SferaTurnMill_T_Z_SUB,
    SferaTurnMill_T_Z_SUB_ER,
    SferaTurnMill_TM_X,
    SferaTurnMill_TM_X_L,
    SferaTurnMill_TM_Z_1,
    SferaTurnMill_TM_Z_2,
    SferaTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.threadmill import (
    ThreadTurnMill_T_Z,
    ThreadTurnMill_T_Z_ER,
    ThreadTurnMill_T_Z_F2,
    ThreadTurnMill_T_Z_SUB,
    ThreadTurnMill_T_Z_SUB_ER,
    ThreadTurnMill_TM_X,
    ThreadTurnMill_TM_X_L,
    ThreadTurnMill_TM_Z_1,
    ThreadTurnMill_TM_Z_2,
    ThreadTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.toroid_mill import (
    ToroidTurnMill_T_Z,
    ToroidTurnMill_T_Z_ER,
    ToroidTurnMill_T_Z_F2,
    ToroidTurnMill_T_Z_SUB,
    ToroidTurnMill_T_Z_SUB_ER,
    ToroidTurnMill_TM_X,
    ToroidTurnMill_TM_X_L,
    ToroidTurnMill_TM_Z_1,
    ToroidTurnMill_TM_Z_2,
    ToroidTurnMill_TM_Z_SUB,
)
from src.tool_updater.classes.tool_classes.milling.vnutr_rad_mill import (
    R_VnutrTurnMill_T_Z,
    R_VnutrTurnMill_T_Z_ER,
    R_VnutrTurnMill_T_Z_F2,
    R_VnutrTurnMill_T_Z_SUB,
    R_VnutrTurnMill_T_Z_SUB_ER,
    R_VnutrTurnMill_TM_X,
    R_VnutrTurnMill_TM_X_L,
    R_VnutrTurnMill_TM_Z_1,
    R_VnutrTurnMill_TM_Z_2,
    R_VnutrTurnMill_TM_Z_SUB,
)


TURN_MILL_DRILLS_HOLDERS = {
    'TM_X': {'tool_class': DrillTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {'tool_class': DrillTurnMill_TM_X_L, 'holder_subdir': 'TM_X_L'},
    'TM_Z_1': {'tool_class': DrillTurnMill_TM_Z_1, 'holder_subdir': 'TM_Z_1'},
    'TM_Z_2': {'tool_class': DrillTurnMill_TM_Z_2, 'holder_subdir': 'TM_Z_2'},
    'TM_Z_SUB': {
        'tool_class': DrillTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {'tool_class': DrillTurnMill_T_Z_ER, 'holder_subdir': 'T_Z_ER'},
    'T_Z_SUB_ER': {
        'tool_class': DrillTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': DrillTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': DrillTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {'tool_class': DrillTurnMill_T_Z_F2, 'holder_subdir': 'T_Z_F2'},
}
TURN_MILL_ENDMILLS_HOLDERS = {
    'TM_X': {'tool_class': KontsTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {'tool_class': KontsTurnMill_TM_X_L, 'holder_subdir': 'TM_X_L'},
    'TM_Z_1': {'tool_class': KontsTurnMill_TM_Z_1, 'holder_subdir': 'TM_Z_1'},
    'TM_Z_2': {'tool_class': KontsTurnMill_TM_Z_2, 'holder_subdir': 'TM_Z_2'},
    'TM_Z_SUB': {
        'tool_class': KontsTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {'tool_class': KontsTurnMill_T_Z_ER, 'holder_subdir': 'T_Z_ER'},
    'T_Z_SUB_ER': {
        'tool_class': KontsTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': KontsTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': KontsTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {'tool_class': KontsTurnMill_T_Z_F2, 'holder_subdir': 'T_Z_F2'},
}
TURN_MILL_BALLMILLS_HOLDERS = {
    'TM_X': {'tool_class': SferaTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {'tool_class': SferaTurnMill_TM_X_L, 'holder_subdir': 'TM_X_L'},
    'TM_Z_1': {'tool_class': SferaTurnMill_TM_Z_1, 'holder_subdir': 'TM_Z_1'},
    'TM_Z_2': {'tool_class': SferaTurnMill_TM_Z_2, 'holder_subdir': 'TM_Z_2'},
    'TM_Z_SUB': {
        'tool_class': SferaTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {'tool_class': SferaTurnMill_T_Z_ER, 'holder_subdir': 'T_Z_ER'},
    'T_Z_SUB_ER': {
        'tool_class': SferaTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': SferaTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': SferaTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {'tool_class': SferaTurnMill_T_Z_F2, 'holder_subdir': 'T_Z_F2'},
}
TURN_MILL_TOROIDMILLS_HOLDERS = {
    'TM_X': {'tool_class': ToroidTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {'tool_class': ToroidTurnMill_TM_X_L, 'holder_subdir': 'TM_X_L'},
    'TM_Z_1': {'tool_class': ToroidTurnMill_TM_Z_1, 'holder_subdir': 'TM_Z_1'},
    'TM_Z_2': {'tool_class': ToroidTurnMill_TM_Z_2, 'holder_subdir': 'TM_Z_2'},
    'TM_Z_SUB': {
        'tool_class': ToroidTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {'tool_class': ToroidTurnMill_T_Z_ER, 'holder_subdir': 'T_Z_ER'},
    'T_Z_SUB_ER': {
        'tool_class': ToroidTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': ToroidTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': ToroidTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {'tool_class': ToroidTurnMill_T_Z_F2, 'holder_subdir': 'T_Z_F2'},
}
TURN_MILL_DISKS_CHAMFER_HOLDERS = {
    'TM_X': {'tool_class': Disk_ChTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': Disk_ChTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': Disk_ChTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': Disk_ChTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': Disk_ChTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': Disk_ChTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': Disk_ChTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': Disk_ChTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': Disk_ChTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': Disk_ChTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_DISKS_ROUNDING_HOLDERS = {
    'TM_X': {'tool_class': Disk_RoTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': Disk_RoTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': Disk_RoTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': Disk_RoTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': Disk_RoTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': Disk_RoTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': Disk_RoTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': Disk_RoTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': Disk_RoTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': Disk_RoTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_DISKS_FLAT_HOLDERS = {
    'TM_X': {'tool_class': Disk_FlTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': Disk_FlTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': Disk_FlTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': Disk_FlTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': Disk_FlTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': Disk_FlTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': Disk_FlTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': Disk_FlTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': Disk_FlTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': Disk_FlTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURNMILL_METCHIKI_BLIND_HOLDERS = {
    'TM_X': {'tool_class': TapBlindTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': TapBlindTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': TapBlindTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': TapBlindTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': TapBlindTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': TapBlindTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': TapBlindTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': TapBlindTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': TapBlindTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': TapBlindTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURNMILL_METCHIKI_THROUGH_HOLDERS = {
    'TM_X': {'tool_class': TapBlindTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': TapBlindTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': TapBlindTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': TapBlindTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': TapBlindTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': TapBlindTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': TapBlindTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': TapBlindTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': TapBlindTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': TapBlindTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_VNUTR_RAD_MILLS_HOLDERS = {
    'TM_X': {'tool_class': R_VnutrTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': R_VnutrTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': R_VnutrTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': R_VnutrTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': R_VnutrTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': R_VnutrTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': R_VnutrTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': R_VnutrTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': R_VnutrTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': R_VnutrTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_CENTROVKI_HOLDERS = {
    'TM_X': {'tool_class': CenterDrillTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': CenterDrillTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': CenterDrillTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': CenterDrillTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': CenterDrillTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': CenterDrillTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': CenterDrillTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': CenterDrillTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': CenterDrillTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': CenterDrillTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_ZENKOVKI_HOLDERS = {
    'TM_X': {'tool_class': CounterSinkTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': CounterSinkTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': CounterSinkTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': CounterSinkTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': CounterSinkTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': CounterSinkTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': CounterSinkTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': CounterSinkTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': CounterSinkTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': CounterSinkTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_CEKOVKI_HOLDERS = {
    'TM_X': {'tool_class': CounterBoreTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': CounterBoreTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': CounterBoreTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': CounterBoreTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': CounterBoreTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': CounterBoreTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': CounterBoreTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': CounterBoreTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': CounterBoreTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': CounterBoreTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_RAZVERTKI_HOLDERS = {
    'TM_X': {'tool_class': ReamerTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {'tool_class': ReamerTurnMill_TM_X_L, 'holder_subdir': 'TM_X_L'},
    'TM_Z_1': {'tool_class': ReamerTurnMill_TM_Z_1, 'holder_subdir': 'TM_Z_1'},
    'TM_Z_2': {'tool_class': ReamerTurnMill_TM_Z_2, 'holder_subdir': 'TM_Z_2'},
    'TM_Z_SUB': {
        'tool_class': ReamerTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {'tool_class': ReamerTurnMill_T_Z_ER, 'holder_subdir': 'T_Z_ER'},
    'T_Z_SUB_ER': {
        'tool_class': ReamerTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': ReamerTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': ReamerTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {'tool_class': ReamerTurnMill_T_Z_F2, 'holder_subdir': 'T_Z_F2'},
}
TURN_MILL_UGLOVIYE_HOLDERS = {
    'TM_X': {'tool_class': ChamferTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': ChamferTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': ChamferTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': ChamferTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': ChamferTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': ChamferTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': ChamferTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': ChamferTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': ChamferTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': ChamferTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_GRIBKOVIE_CHAMFER_HOLDERS = {
    'TM_X': {'tool_class': Grib_ChTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': Grib_ChTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': Grib_ChTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': Grib_ChTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': Grib_ChTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': Grib_ChTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': Grib_ChTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': Grib_ChTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': Grib_ChTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': Grib_ChTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_GRIBKOVIE_ROUNDING_HOLDERS = {
    'TM_X': {'tool_class': Grib_RoTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': Grib_RoTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': Grib_RoTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': Grib_RoTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': Grib_RoTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': Grib_RoTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': Grib_RoTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': Grib_RoTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': Grib_RoTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': Grib_RoTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_GRIBKOVIE_FLAT_HOLDERS = {
    'TM_X': {'tool_class': Grib_FlTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {
        'tool_class': Grib_FlTurnMill_TM_X_L,
        'holder_subdir': 'TM_X_L',
    },
    'TM_Z_1': {
        'tool_class': Grib_FlTurnMill_TM_Z_1,
        'holder_subdir': 'TM_Z_1',
    },
    'TM_Z_2': {
        'tool_class': Grib_FlTurnMill_TM_Z_2,
        'holder_subdir': 'TM_Z_2',
    },
    'TM_Z_SUB': {
        'tool_class': Grib_FlTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {
        'tool_class': Grib_FlTurnMill_T_Z_ER,
        'holder_subdir': 'T_Z_ER',
    },
    'T_Z_SUB_ER': {
        'tool_class': Grib_FlTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': Grib_FlTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': Grib_FlTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {
        'tool_class': Grib_FlTurnMill_T_Z_F2,
        'holder_subdir': 'T_Z_F2',
    },
}
TURN_MILL_REZBOFREZI_HOLDERS = {
    'TM_X': {'tool_class': ThreadTurnMill_TM_X, 'holder_subdir': 'TM_X'},
    'TM_X_L': {'tool_class': ThreadTurnMill_TM_X_L, 'holder_subdir': 'TM_X_L'},
    'TM_Z_1': {'tool_class': ThreadTurnMill_TM_Z_1, 'holder_subdir': 'TM_Z_1'},
    'TM_Z_2': {'tool_class': ThreadTurnMill_TM_Z_2, 'holder_subdir': 'TM_Z_2'},
    'TM_Z_SUB': {
        'tool_class': ThreadTurnMill_TM_Z_SUB,
        'holder_subdir': 'TM_Z_SUB',
    },
    'T_Z_ER': {'tool_class': ThreadTurnMill_T_Z_ER, 'holder_subdir': 'T_Z_ER'},
    'T_Z_SUB_ER': {
        'tool_class': ThreadTurnMill_T_Z_SUB_ER,
        'holder_subdir': 'T_Z_SUB_ER',
    },
    'T_Z': {'tool_class': ThreadTurnMill_T_Z, 'holder_subdir': 'T_Z'},
    'T_Z_SUB': {
        'tool_class': ThreadTurnMill_T_Z_SUB,
        'holder_subdir': 'T_Z_SUB',
    },
    'T_Z_F2': {'tool_class': ThreadTurnMill_T_Z_F2, 'holder_subdir': 'T_Z_F2'},
}
