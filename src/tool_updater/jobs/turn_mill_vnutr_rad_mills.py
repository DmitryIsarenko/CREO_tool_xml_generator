"""Catalog jobs for turn_mill_vnutr_rad_mills."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_VNUTR_RAD_MILLS_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_vnutr_rad_mills() -> list[GenerationJob]:
    """Build jobs for the turn_mill_vnutr_rad_mills group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_VNUTR_RAD_MILLS_HOLDERS
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
                / 'VnutrRadMill'
                / 'Precitool 178815',
                teeth_num=4,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'vnutr_rad_',
                file_name_suffix='_178815',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'internal_R'
                / 'Precitool'
                / '178815'
                / '178815_cut_data.json',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'internal_R'
                / 'Precitool'
                / '178815'
                / '178815.json',
            )
        )
    return jobs
