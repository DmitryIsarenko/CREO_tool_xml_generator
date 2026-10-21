"""Catalog jobs for toroidmills."""

from src.tool_updater.classes.tool_classes.milling.toroid_mill import (
    ToroidMill,
)
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def toroidmills() -> list[GenerationJob]:
    """Build jobs for the toroidmills group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=ToroidMill,
            target_path=OUTPUT_DIR / 'ToroidMill' / 'Gesac UA100-R3',
            debug_mode=0,
            file_name_prefix='fr_tor_',
            teeth_num=3,
            file_name_suffix='_UA100-R3',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'toroidal_endmills'
            / 'Gesac'
            / 'isoN'
            / 'UA100-R3'
            / 'UA100-R3.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'toroidal_endmills'
            / 'Gesac'
            / 'isoN'
            / 'UA100-R3'
            / 'UA100-R3_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=ToroidMill,
            target_path=OUTPUT_DIR / 'ToroidMill' / 'Gesac SS600-R4',
            debug_mode=0,
            file_name_prefix='fr_tor_',
            teeth_num=4,
            file_name_suffix='_SS600-R4',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'toroidal_endmills'
            / 'Gesac'
            / 'isoP_isoM'
            / 'SS600-R4'
            / 'SS600-R4.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'toroidal_endmills'
            / 'Gesac'
            / 'isoP_isoM'
            / 'SS600-R4'
            / 'SS600-R4_cut_data.json',
        )
    )
    return jobs
