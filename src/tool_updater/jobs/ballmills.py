"""Catalog jobs for ballmills."""

from src.tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def ballmills() -> list[GenerationJob]:
    """Build jobs for the ballmills group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=BallMill,
            target_path=OUTPUT_DIR / 'BallMill' / 'Gesac UA100-B2',
            debug_mode=0,
            file_name_prefix='sfera_',
            teeth_num=2,
            file_name_suffix='_UA100-B2',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'ballnose_mills'
            / 'Gesac'
            / 'UA100-B2'
            / 'UA100-B2.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'ballnose_mills'
            / 'Gesac'
            / 'UA100-B2'
            / 'UA100-B2_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=BallMill,
            target_path=OUTPUT_DIR / 'BallMill' / 'Gesac SS600-B4',
            debug_mode=0,
            file_name_prefix='sfera_',
            teeth_num=4,
            file_name_suffix='_SS600-B4',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'ballnose_mills'
            / 'Gesac'
            / 'SS600-B4'
            / 'SS600-B4.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'ballnose_mills'
            / 'Gesac'
            / 'SS600-B4'
            / 'SS600-B4_cut_data.json',
        )
    )
    return jobs
