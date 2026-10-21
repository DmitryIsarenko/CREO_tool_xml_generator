"""Catalog jobs for turn_mill_centrovki."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_CENTROVKI_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_centrovki() -> list[GenerationJob]:
    """Build jobs for the turn_mill_centrovki group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_CENTROVKI_HOLDERS
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
                / 'CenterDrill'
                / 'Precitool 105200',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'centr_',
                file_name_suffix='_105200',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'center_drills'
                / 'Precitool'
                / '105200'
                / '105200.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'center_drills'
                / 'Precitool'
                / '105200'
                / '105200_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'CenterDrill'
                / 'Precitool 105600L',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'centr_udlin_',
                file_name_suffix='_105600L',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'axial'
                / 'center_drills'
                / 'Precitool'
                / '105600L - extended'
                / '105600L.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'axial'
                / 'center_drills'
                / 'Precitool'
                / '105600L - extended'
                / '105600L_cut_data.json',
            )
        )
    return jobs
