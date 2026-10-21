"""Catalog jobs for rezbofrezi."""

from src.tool_updater.classes.tool_classes.milling.threadmill import ThreadMill
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def rezbofrezi() -> list[GenerationJob]:
    """Build jobs for the rezbofrezi group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=ThreadMill,
            target_path=OUTPUT_DIR / 'ThreadMill' / 'Vardex Metric Helicool',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='rezbofr_',
            file_name_suffix='_helicool',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'thread_milling'
            / 'Vardex'
            / 'Helicool'
            / 'metric'
            / 'helicool_m.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'thread_milling'
            / 'Vardex'
            / 'Helicool'
            / 'metric'
            / 'helicool_m_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=ThreadMill,
            target_path=OUTPUT_DIR / 'ThreadMill' / 'Vardex Inch Helicool',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='rezbofr_',
            file_name_suffix='_helicool',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'thread_milling'
            / 'Vardex'
            / 'Helicool'
            / 'inch'
            / 'helicool_g.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'thread_milling'
            / 'Vardex'
            / 'Helicool'
            / 'inch'
            / 'helicool_g_cut_data.json',
        )
    )
    return jobs
