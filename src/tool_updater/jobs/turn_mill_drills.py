"""Catalog jobs for turn_mill_drills."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_DRILLS_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_drills() -> list[GenerationJob]:
    """Build jobs for the turn_mill_drills group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_DRILLS_HOLDERS
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
                / 'Drill'
                / 'Osawa 2386STI',
                debug_mode=0,
                teeth_num=1,
                file_name_prefix=tool_prefix + 'sv_',
                file_name_suffix='_2386STI',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'drills'
                / 'Osawa'
                / 'hss_regular_drills'
                / '2386STI.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'drills'
                / 'Osawa'
                / 'hss_regular_drills'
                / '2386STI_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'Drill'
                / 'Osawa 1692LS',
                debug_mode=0,
                teeth_num=1,
                file_name_prefix=tool_prefix + 'sv_udlin_',
                file_name_suffix='_1692LS',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'drills'
                / 'Osawa'
                / 'hss_extended_drills'
                / '1692LS.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'drills'
                / 'Osawa'
                / 'hss_extended_drills'
                / '1692LS_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'Drill'
                / 'China Extended',
                debug_mode=0,
                teeth_num=1,
                file_name_prefix=tool_prefix + 'sv_udlin_',
                file_name_suffix='_China',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'drills'
                / 'China'
                / '1 geom.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'drills'
                / 'China'
                / '2 cut_data.json',
            )
        )
    return jobs
