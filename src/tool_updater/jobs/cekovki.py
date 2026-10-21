"""Catalog jobs for cekovki."""

from src.tool_updater.classes.tool_classes.axial.counterbore import CounterBore
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def cekovki() -> list[GenerationJob]:
    """Build jobs for the cekovki group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=CounterBore,
            target_path=OUTPUT_DIR / 'CounterBore' / 'Precitool 111010',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='cekov_',
            file_name_suffix='_111010',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'counterbores'
            / 'Precitool'
            / '111010'
            / '111010.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'counterbores'
            / 'Precitool'
            / '111010'
            / '111010_cut_data.json',
        )
    )
    return jobs
