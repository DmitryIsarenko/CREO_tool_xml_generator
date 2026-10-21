"""Catalog jobs for index_mills."""

from src.tool_updater.classes.tool_classes.milling.index_mill import (
    IndexMillSingleASMs,
)
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def index_mills() -> list[GenerationJob]:
    """Build jobs for the index_mills group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=IndexMillSingleASMs,
            target_path=OUTPUT_DIR / 'IndexMill' / 'Taegu Tec' / '3P TE90-10',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='',
            file_name_suffix=' Taegu Tec',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Taegu Tec'
            / '3P TE90-10'
            / '3_geom.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Taegu Tec'
            / '3P TE90-10'
            / '4_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=IndexMillSingleASMs,
            target_path=OUTPUT_DIR / 'IndexMill' / 'Taegu Tec' / '3P TE90-15',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='',
            file_name_suffix=' Taegu Tec',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Taegu Tec'
            / '3P TE90-15'
            / '3_geom.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Taegu Tec'
            / '3P TE90-15'
            / '4_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=IndexMillSingleASMs,
            target_path=OUTPUT_DIR / 'IndexMill' / 'Taegu Tec' / '3P TF90-15',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='',
            file_name_suffix=' Taegu Tec',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Taegu Tec'
            / '3P TF90-15'
            / '3_geom.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Taegu Tec'
            / '3P TF90-15'
            / '4_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=IndexMillSingleASMs,
            target_path=OUTPUT_DIR / 'IndexMill' / 'Mitsubishi' / 'AJX',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='',
            file_name_suffix=' Mitsubishi',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Mitsubishi'
            / 'AJX'
            / '3_geom.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Mitsubishi'
            / 'AJX'
            / '4_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=IndexMillSingleASMs,
            target_path=OUTPUT_DIR / 'IndexMill' / 'Mitsubishi' / 'APX3000',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='',
            file_name_suffix=' Mitsubishi',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Mitsubishi'
            / 'APX3000'
            / '3_geom.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'index_mills'
            / 'Mitsubishi'
            / 'APX3000'
            / '4_cut_data.json',
        )
    )
    return jobs
