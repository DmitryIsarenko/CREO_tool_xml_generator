"""Catalog jobs for turn_mill_razvertki."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_RAZVERTKI_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_razvertki() -> list[GenerationJob]:
    """Build jobs for the turn_mill_razvertki group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_RAZVERTKI_HOLDERS
    for holder in all_holders:
        holder_subdir = all_holders[holder]['holder_subdir']
        tool_class = all_holders[holder]['tool_class']
        tool_prefix = holder_subdir.lower() + '_'
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'Reamer'
                / 'Guhring 1409',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'razvert_',
                file_name_suffix='_1409',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'reamers'
                / 'Guhring'
                / '1409'
                / '1409.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'reamers'
                / 'Guhring'
                / '1409'
                / '1409_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'Reamer'
                / 'Garant 162961',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'razvert_udlin_',
                file_name_suffix='_162961',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'reamers'
                / 'Garant'
                / '162961'
                / '162961.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'reamers'
                / 'Garant'
                / '162961'
                / '162961_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'Reamer'
                / 'Guhring 1411',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'razvert_',
                file_name_suffix='_1411',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'reamers'
                / 'Guhring'
                / '1411'
                / '1411.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'reamers'
                / 'Guhring'
                / '1411'
                / '1411_cut_data.json',
            )
        )
    return jobs
