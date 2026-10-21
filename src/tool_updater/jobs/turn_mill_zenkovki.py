"""Catalog jobs for turn_mill_zenkovki."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_ZENKOVKI_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_zenkovki() -> list[GenerationJob]:
    """Build jobs for the turn_mill_zenkovki group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_ZENKOVKI_HOLDERS
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
                / 'CounterSink'
                / 'Precitool 110120',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'zenk_',
                file_name_suffix='_110120',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'countersinks'
                / 'Precitool'
                / '110120'
                / '110120.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'countersinks'
                / 'Precitool'
                / '110120'
                / '110120_cut_data.json',
            )
        )
    return jobs
