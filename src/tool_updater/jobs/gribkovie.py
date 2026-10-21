"""Catalog jobs for gribkovie."""

from src.tool_updater.classes.tool_classes.milling.grib_mill import (
    GribMillChamfer,
    GribMillRounding,
)
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def gribkovie() -> list[GenerationJob]:
    """Build jobs for the gribkovie group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=GribMillRounding,
            target_path=OUTPUT_DIR / 'GribMill' / 'Iscar MM GRIT',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='grib_',
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
            tool_class=GribMillChamfer,
            target_path=OUTPUT_DIR / 'GribMill' / 'Iscar MM GRIT-45A',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='grib_',
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
            tool_class=GribMillRounding,
            target_path=OUTPUT_DIR / 'GribMill' / 'Iscar MM TS-H',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='grib_',
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
            tool_class=GribMillRounding,
            target_path=OUTPUT_DIR / 'GribMill' / 'Iscar MM TS-N rounding',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='grib_',
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
    jobs.append(
        GenerationJob(
            tool_class=GribMillChamfer,
            target_path=OUTPUT_DIR / 'GribMill' / 'Iscar MM TS-N chamfer',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='grib_',
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
