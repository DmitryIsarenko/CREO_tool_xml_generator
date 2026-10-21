"""Catalog jobs for turnmill_metchiki_through."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURNMILL_METCHIKI_THROUGH_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turnmill_metchiki_through() -> list[GenerationJob]:
    """Build jobs for the turnmill_metchiki_through group."""
    jobs: list[GenerationJob] = []
    all_holders = TURNMILL_METCHIKI_THROUGH_HOLDERS
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
                / 'Tap'
                / 'Garant Metric through 132640',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'metchik_skvozn_',
                file_name_suffix='_132640',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'metric'
                / 'through_hole'
                / '132640'
                / '132640.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'metric'
                / 'through_hole'
                / '132640'
                / '132640_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'Tap'
                / 'Garant Inch through 133300',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'metchik_skvozn_',
                file_name_suffix='_133300',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'inch'
                / 'through_hole'
                / '133300'
                / '133300.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'inch'
                / 'through_hole'
                / '133300'
                / '133300_cut_data.json',
            )
        )
    return jobs
