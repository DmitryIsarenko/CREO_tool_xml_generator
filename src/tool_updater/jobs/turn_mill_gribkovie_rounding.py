"""Catalog jobs for turn_mill_gribkovie_rounding."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_GRIBKOVIE_ROUNDING_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_gribkovie_rounding() -> list[GenerationJob]:
    """Build jobs for the turn_mill_gribkovie_rounding group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_GRIBKOVIE_ROUNDING_HOLDERS
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
                / 'GribMill'
                / 'Iscar MM GRIT',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'grib_',
                file_name_suffix='_GRIT',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'GRIT'
                / 'GRIT.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'GRIT'
                / 'GRIT_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'GribMill'
                / 'Iscar MM TS-H',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'grib_',
                file_name_suffix='_TS-H',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'TS-H'
                / 'TS-H.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'TS-H'
                / 'TS-H_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'GribMill'
                / 'Iscar MM TS-N rounding',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'grib_',
                file_name_suffix='_TS-N',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'TS-N rounding'
                / 'TS-N.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'TS-N rounding'
                / 'TS-N_cut_data.json',
            )
        )
    return jobs
