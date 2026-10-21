"""Catalog jobs for turn_mill_rezbofrezi."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_REZBOFREZI_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_rezbofrezi() -> list[GenerationJob]:
    """Build jobs for the turn_mill_rezbofrezi group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_REZBOFREZI_HOLDERS
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
                / 'ThreadMill'
                / 'Vardex Metric Helicool',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'rezbofr_',
                file_name_suffix='_helicool',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'thread_milling'
                / 'Vardex'
                / 'Helicool'
                / 'metric'
                / 'helicool_m.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'thread_milling'
                / 'Vardex'
                / 'Helicool'
                / 'metric'
                / 'helicool_m_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'ThreadMill'
                / 'Vardex Inch Helicool',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'rezbofr_',
                file_name_suffix='_helicool',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'thread_milling'
                / 'Vardex'
                / 'Helicool'
                / 'inch'
                / 'helicool_g.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'thread_milling'
                / 'Vardex'
                / 'Helicool'
                / 'inch'
                / 'helicool_g_cut_data.json',
            )
        )
    return jobs
