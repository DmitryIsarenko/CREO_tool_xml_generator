"""Catalog jobs for metchiki."""

from src.tool_updater.classes.tool_classes.axial.tap import (
    TapBlind,
    TapThrough,
)
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def metchiki() -> list[GenerationJob]:
    """Build jobs for the metchiki group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=TapBlind,
            target_path=OUTPUT_DIR / 'Tap' / 'Garant Metric Blind 135850',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='metchik_gluh_',
            file_name_suffix='_135850',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'metric'
            / 'blind_hole'
            / '135850'
            / '135850.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'metric'
            / 'blind_hole'
            / '135850'
            / '135850_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=TapThrough,
            target_path=OUTPUT_DIR / 'Tap' / 'Garant Metric through 132640',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='metchik_skvozn_',
            file_name_suffix='_132640',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'metric'
            / 'through_hole'
            / '132640'
            / '132640.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'metric'
            / 'through_hole'
            / '132640'
            / '132640_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=TapBlind,
            target_path=OUTPUT_DIR / 'Tap' / 'Garant Inch blind 137805',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='metchik_gluh_',
            file_name_suffix='_137805',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'inch'
            / 'blind_hole'
            / '137805'
            / '137805.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'inch'
            / 'blind_hole'
            / '137805'
            / '137805_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=TapThrough,
            target_path=OUTPUT_DIR / 'Tap' / 'Garant Inch through 133300',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='metchik_skvozn_',
            file_name_suffix='_133300',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'inch'
            / 'through_hole'
            / '133300'
            / '133300.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'axial'
            / 'taps'
            / 'Garant'
            / 'inch'
            / 'through_hole'
            / '133300'
            / '133300_cut_data.json',
        )
    )
    return jobs
