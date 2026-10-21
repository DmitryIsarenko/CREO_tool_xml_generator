"""Catalog jobs for turnmill_metchiki_blind."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURNMILL_METCHIKI_BLIND_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turnmill_metchiki_blind() -> list[GenerationJob]:
    """Build jobs for the turnmill_metchiki_blind group."""
    jobs: list[GenerationJob] = []
    all_holders = TURNMILL_METCHIKI_BLIND_HOLDERS
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
                / 'Garant Metric Blind 135850',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'metchik_gluh_',
                file_name_suffix='_135850',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'metric'
                / 'blind_hole'
                / '135850'
                / '135850.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'metric'
                / 'blind_hole'
                / '135850'
                / '135850_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'Tap'
                / 'Garant Inch blind 137805',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'metchik_gluh_',
                file_name_suffix='_137805',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'inch'
                / 'blind_hole'
                / '137805'
                / '137805.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'taps'
                / 'Garant'
                / 'inch'
                / 'blind_hole'
                / '137805'
                / '137805_cut_data.json',
            )
        )
    return jobs
