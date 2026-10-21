"""Catalog jobs for vnutr_rad_mills."""

from src.tool_updater.classes.tool_classes.milling.vnutr_rad_mill import (
    VnutrRadMill,
)
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def vnutr_rad_mills() -> list[GenerationJob]:
    """Build jobs for the vnutr_rad_mills group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=VnutrRadMill,
            target_path=OUTPUT_DIR / 'VnutrRadMill' / 'Precitool 178815',
            teeth_num=4,
            debug_mode=0,
            file_name_prefix='vnutr_rad_',
            file_name_suffix='_178815',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'internal_R'
            / 'Precitool'
            / '178815'
            / '178815_cut_data.json',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'internal_R'
            / 'Precitool'
            / '178815'
            / '178815.json',
        )
    )
    return jobs
