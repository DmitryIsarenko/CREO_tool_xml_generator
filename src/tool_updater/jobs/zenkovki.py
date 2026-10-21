"""Catalog jobs for zenkovki."""

from src.tool_updater.classes.tool_classes.axial.countersink import CounterSink
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def zenkovki() -> list[GenerationJob]:
    """Build jobs for the zenkovki group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=CounterSink,
            target_path=OUTPUT_DIR / 'CounterSink' / 'Precitool 110120',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='zenk_',
            file_name_suffix='_110120',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'countersinks'
            / 'Precitool'
            / '110120'
            / '110120.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'countersinks'
            / 'Precitool'
            / '110120'
            / '110120_cut_data.json',
        )
    )
    return jobs
