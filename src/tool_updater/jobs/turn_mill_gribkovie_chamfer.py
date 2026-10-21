"""Catalog jobs for turn_mill_gribkovie_chamfer."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_GRIBKOVIE_CHAMFER_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_gribkovie_chamfer() -> list[GenerationJob]:
    """Build jobs for the turn_mill_gribkovie_chamfer group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_GRIBKOVIE_CHAMFER_HOLDERS
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
                / 'Iscar MM GRIT-45A',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'grib_',
                file_name_suffix='_GRIT-45A',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'GRIT-45A'
                / 'GRIT-45A.json',
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
                / 'Iscar MM TS-N chamfer',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'grib_',
                file_name_suffix='_TS-N',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'TS-N chamfer'
                / 'TS-N.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'gribkovie'
                / 'Iscar'
                / 'MultiMaster'
                / 'TS-N chamfer'
                / 'TS-N_cut_data.json',
            )
        )
    return jobs
