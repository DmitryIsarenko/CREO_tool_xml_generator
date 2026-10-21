"""Catalog jobs for centrovki."""

from src.tool_updater.classes.tool_classes.axial.centerdrill import CenterDrill
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def centrovki() -> list[GenerationJob]:
    """Build jobs for the centrovki group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=CenterDrill,
            target_path=OUTPUT_DIR / 'CenterDrill' / 'Precitool 105200',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='centr_',
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
            tool_class=CenterDrill,
            target_path=OUTPUT_DIR / 'CenterDrill' / 'Precitool 105600L',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='centr_udlin_',
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
