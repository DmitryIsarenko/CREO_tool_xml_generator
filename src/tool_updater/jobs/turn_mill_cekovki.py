"""Catalog jobs for turn_mill_cekovki."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_CEKOVKI_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_cekovki() -> list[GenerationJob]:
    """Build jobs for the turn_mill_cekovki group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_CEKOVKI_HOLDERS
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
                / 'CounterBore'
                / 'Precitool 111010',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'cekov_',
                file_name_suffix='_111010',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'counterbores'
                / 'Precitool'
                / '111010'
                / '111010.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'counterbores'
                / 'Precitool'
                / '111010'
                / '111010_cut_data.json',
            )
        )
    return jobs
