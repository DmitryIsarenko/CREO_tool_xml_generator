"""Available catalog job groups."""

from collections.abc import Callable

from src.tool_updater.jobs.ballmills import ballmills
from src.tool_updater.jobs.cekovki import cekovki
from src.tool_updater.jobs.centrovki import centrovki
from src.tool_updater.jobs.disk_mills import disk_mills
from src.tool_updater.jobs.drills import drills
from src.tool_updater.jobs.endmills import endmills
from src.tool_updater.jobs.gribkovie import gribkovie
from src.tool_updater.jobs.index_mills import index_mills
from src.tool_updater.jobs.metchiki import metchiki
from src.tool_updater.jobs.model import GenerationJob
from src.tool_updater.jobs.razvertki import razvertki
from src.tool_updater.jobs.rezbofrezi import rezbofrezi
from src.tool_updater.jobs.toroidmills import toroidmills
from src.tool_updater.jobs.turn_mill_ballmills import turn_mill_ballmills
from src.tool_updater.jobs.turn_mill_cekovki import turn_mill_cekovki
from src.tool_updater.jobs.turn_mill_centrovki import turn_mill_centrovki
from src.tool_updater.jobs.turn_mill_disks import turn_mill_disks
from src.tool_updater.jobs.turn_mill_disks_chamfer import (
    turn_mill_disks_chamfer,
)
from src.tool_updater.jobs.turn_mill_disks_flat import turn_mill_disks_flat
from src.tool_updater.jobs.turn_mill_disks_rounding import (
    turn_mill_disks_rounding,
)
from src.tool_updater.jobs.turn_mill_drills import turn_mill_drills
from src.tool_updater.jobs.turn_mill_endmills import turn_mill_endmills
from src.tool_updater.jobs.turn_mill_gribkovie import turn_mill_gribkovie
from src.tool_updater.jobs.turn_mill_gribkovie_chamfer import (
    turn_mill_gribkovie_chamfer,
)
from src.tool_updater.jobs.turn_mill_gribkovie_flat import (
    turn_mill_gribkovie_flat,
)
from src.tool_updater.jobs.turn_mill_gribkovie_rounding import (
    turn_mill_gribkovie_rounding,
)
from src.tool_updater.jobs.turn_mill_razvertki import turn_mill_razvertki
from src.tool_updater.jobs.turn_mill_rezbofrezi import turn_mill_rezbofrezi
from src.tool_updater.jobs.turn_mill_toroidmills import turn_mill_toroidmills
from src.tool_updater.jobs.turn_mill_ugloviye import turn_mill_ugloviye
from src.tool_updater.jobs.turn_mill_vnutr_rad_mills import (
    turn_mill_vnutr_rad_mills,
)
from src.tool_updater.jobs.turn_mill_zenkovki import turn_mill_zenkovki
from src.tool_updater.jobs.turnmill_metchiki import turnmill_metchiki
from src.tool_updater.jobs.turnmill_metchiki_blind import (
    turnmill_metchiki_blind,
)
from src.tool_updater.jobs.turnmill_metchiki_through import (
    turnmill_metchiki_through,
)
from src.tool_updater.jobs.ugloviye import ugloviye
from src.tool_updater.jobs.vnutr_rad_mills import vnutr_rad_mills
from src.tool_updater.jobs.zenkovki import zenkovki


JOB_BUILDERS: dict[str, Callable[[], list[GenerationJob]]] = {
    'drills': drills,
    'turn_mill_drills': turn_mill_drills,
    'endmills': endmills,
    'turn_mill_endmills': turn_mill_endmills,
    'ballmills': ballmills,
    'turn_mill_ballmills': turn_mill_ballmills,
    'toroidmills': toroidmills,
    'turn_mill_toroidmills': turn_mill_toroidmills,
    'disk_mills': disk_mills,
    'turn_mill_disks': turn_mill_disks,
    'turn_mill_disks_chamfer': turn_mill_disks_chamfer,
    'turn_mill_disks_rounding': turn_mill_disks_rounding,
    'turn_mill_disks_flat': turn_mill_disks_flat,
    'zenkovki': zenkovki,
    'centrovki': centrovki,
    'metchiki': metchiki,
    'turnmill_metchiki': turnmill_metchiki,
    'turnmill_metchiki_blind': turnmill_metchiki_blind,
    'turnmill_metchiki_through': turnmill_metchiki_through,
    'vnutr_rad_mills': vnutr_rad_mills,
    'turn_mill_vnutr_rad_mills': turn_mill_vnutr_rad_mills,
    'razvertki': razvertki,
    'cekovki': cekovki,
    'turn_mill_centrovki': turn_mill_centrovki,
    'turn_mill_zenkovki': turn_mill_zenkovki,
    'turn_mill_cekovki': turn_mill_cekovki,
    'turn_mill_razvertki': turn_mill_razvertki,
    'ugloviye': ugloviye,
    'turn_mill_ugloviye': turn_mill_ugloviye,
    'gribkovie': gribkovie,
    'turn_mill_gribkovie': turn_mill_gribkovie,
    'turn_mill_gribkovie_chamfer': turn_mill_gribkovie_chamfer,
    'turn_mill_gribkovie_rounding': turn_mill_gribkovie_rounding,
    'turn_mill_gribkovie_flat': turn_mill_gribkovie_flat,
    'rezbofrezi': rezbofrezi,
    'turn_mill_rezbofrezi': turn_mill_rezbofrezi,
    'index_mills': index_mills,
}
