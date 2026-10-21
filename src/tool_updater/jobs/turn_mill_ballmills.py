"""Catalog jobs for turn_mill_ballmills."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_BALLMILLS_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_ballmills() -> list[GenerationJob]:
    """Build jobs for the turn_mill_ballmills group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_BALLMILLS_HOLDERS
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
                / 'BallMill'
                / 'Gesac UA100-B2',
                debug_mode=0,
                file_name_prefix=tool_prefix + 'sfera_',
                teeth_num=2,
                file_name_suffix='_UA100-B2',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'ballnose_mills'
                / 'Gesac'
                / 'UA100-B2'
                / 'UA100-B2.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'ballnose_mills'
                / 'Gesac'
                / 'UA100-B2'
                / 'UA100-B2_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'BallMill'
                / 'Gesac SS600-B4',
                debug_mode=0,
                file_name_prefix=tool_prefix + 'sfera_',
                teeth_num=4,
                file_name_suffix='_SS600-B4',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'ballnose_mills'
                / 'Gesac'
                / 'SS600-B4'
                / 'SS600-B4.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'ballnose_mills'
                / 'Gesac'
                / 'SS600-B4'
                / 'SS600-B4_cut_data.json',
            )
        )
    return jobs
