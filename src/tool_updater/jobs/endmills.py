"""Catalog jobs for endmills."""

from src.tool_updater.classes.tool_classes.milling.endmill import EndMill
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def endmills() -> list[GenerationJob]:
    """Build jobs for the endmills group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=EndMill,
            target_path=OUTPUT_DIR / 'EndMill' / 'Gesac UA100-S2',
            debug_mode=0,
            file_name_prefix='fr_univ_',
            teeth_num=2,
            file_name_suffix='_UA100-S2',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoN'
            / 'UA100-S2'
            / 'UA100-S2.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoN'
            / 'UA100-S2'
            / 'UA100-S2_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=EndMill,
            target_path=OUTPUT_DIR / 'EndMill' / 'Gesac UA100-S3',
            debug_mode=0,
            file_name_prefix='fr_univ_',
            teeth_num=3,
            file_name_suffix='_UA100-S3',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoN'
            / 'UA100-S3'
            / 'UA100-S3.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoN'
            / 'UA100-S3'
            / 'UA100-S3_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=EndMill,
            target_path=OUTPUT_DIR / 'EndMill' / 'Gesac UH360-S4',
            debug_mode=0,
            file_name_prefix='fr_univ_',
            teeth_num=4,
            file_name_suffix='_UH360-S4',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoP_iso_M'
            / 'SS600-S4(UH360-S4)'
            / 'SS600-S4(UH360-S4).json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoP_iso_M'
            / 'SS600-S4(UH360-S4)'
            / 'SS600-S4(UH360-S4)_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=EndMill,
            target_path=OUTPUT_DIR / 'EndMill' / 'Gesac STR340-S4',
            debug_mode=0,
            file_name_prefix='fr_chern_',
            teeth_num=4,
            file_name_suffix='_STR340-S4',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'rough_isoP_isoM'
            / 'UPR210-S4(STR340-S4)'
            / 'UPR210-S4(STR340-S4).json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'rough_isoP_isoM'
            / 'UPR210-S4(STR340-S4)'
            / 'UPR210-S4(STR340-S4)_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=EndMill,
            target_path=OUTPUT_DIR / 'EndMill' / 'Gesac UA100-SL3',
            debug_mode=0,
            file_name_prefix='fr_konts_udlin_',
            teeth_num=3,
            file_name_suffix='_UA100-SL3',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoN'
            / 'UA100-SL3'
            / 'UA100-SL3.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoN'
            / 'UA100-SL3'
            / 'UA100-SL3_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=EndMill,
            target_path=OUTPUT_DIR / 'EndMill' / 'Gesac UP210-SL4',
            debug_mode=0,
            file_name_prefix='fr_konts_udlin_',
            teeth_num=4,
            file_name_suffix='_UP210-SL4',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoP_iso_M'
            / 'SS600-SL4(UP210-SL4)'
            / 'SS600-SL4(UP210-SL4).json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'endmills'
            / 'Gesac'
            / 'univ_isoP_iso_M'
            / 'SS600-SL4(UP210-SL4)'
            / 'SS600-SL4(UP210-SL4)_cut_data.json',
        )
    )
    return jobs
