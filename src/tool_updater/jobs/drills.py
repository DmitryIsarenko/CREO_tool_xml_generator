"""Catalog jobs for drills."""

from src.tool_updater.classes.tool_classes.axial.drill import Drill
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def drills() -> list[GenerationJob]:
    """Build jobs for the drills group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=Drill,
            target_path=OUTPUT_DIR / 'Drill' / 'Osawa 2386STI',
            debug_mode=0,
            teeth_num=1,
            file_name_prefix='sv_',
            file_name_suffix='_2386STI',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'drills'
            / 'Osawa'
            / 'hss_regular_drills'
            / '2386STI.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'drills'
            / 'Osawa'
            / 'hss_regular_drills'
            / '2386STI_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=Drill,
            target_path=OUTPUT_DIR / 'Drill' / 'Osawa 1692LS',
            debug_mode=0,
            teeth_num=1,
            file_name_prefix='sv_udlin_',
            file_name_suffix='_1692LS',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'drills'
            / 'Osawa'
            / 'hss_extended_drills'
            / '1692LS.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'drills'
            / 'Osawa'
            / 'hss_extended_drills'
            / '1692LS_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=Drill,
            target_path=OUTPUT_DIR / 'Drill' / 'China Extended',
            debug_mode=0,
            teeth_num=1,
            file_name_prefix='sv_udlin_',
            file_name_suffix='_China',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'drills'
            / 'China'
            / '1 geom.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'drills'
            / 'China'
            / '2 cut_data.json',
        )
    )
    return jobs
