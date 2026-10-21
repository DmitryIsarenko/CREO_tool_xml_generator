"""Catalog jobs for ugloviye."""

from src.tool_updater.classes.tool_classes.milling.chamfer_mill import (
    ChamferMill,
)
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def ugloviye() -> list[GenerationJob]:
    """Build jobs for the ugloviye group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=ChamferMill,
            target_path=OUTPUT_DIR / 'ChamferMill' / 'Gesac UP210-L60',
            teeth_num=4,
            debug_mode=0,
            file_name_prefix='uglovaya_',
            file_name_suffix='_UP210-L60',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'Gesac'
            / 'UP210'
            / 'UP210-L60.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'Gesac'
            / 'UP210'
            / 'UP210-L60_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=ChamferMill,
            target_path=OUTPUT_DIR / 'ChamferMill' / 'Gesac UP210-L90',
            teeth_num=4,
            debug_mode=0,
            file_name_prefix='uglovaya_',
            file_name_suffix='_UP210-L90',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'Gesac'
            / 'UP210'
            / 'UP210-L90.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'Gesac'
            / 'UP210'
            / 'UP210-L90_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=ChamferMill,
            target_path=OUTPUT_DIR / 'ChamferMill' / 'Gesac UP210-L120',
            teeth_num=4,
            debug_mode=0,
            file_name_prefix='uglovaya_',
            file_name_suffix='_UP210-L120',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'Gesac'
            / 'UP210'
            / 'UP210-L120.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'Gesac'
            / 'UP210'
            / 'UP210-L120_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=ChamferMill,
            target_path=OUTPUT_DIR / 'ChamferMill' / 'Special A30',
            teeth_num=4,
            debug_mode=0,
            file_name_prefix='uglovaya_',
            file_name_suffix='_A30',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'special'
            / 'L30.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'special'
            / 'L30_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=ChamferMill,
            target_path=OUTPUT_DIR / 'ChamferMill' / 'Special A45',
            teeth_num=4,
            debug_mode=0,
            file_name_prefix='uglovaya_',
            file_name_suffix='_A45',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'special'
            / 'L45.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'chamfer_mills'
            / 'special'
            / 'L45_cut_data.json',
        )
    )
    return jobs
