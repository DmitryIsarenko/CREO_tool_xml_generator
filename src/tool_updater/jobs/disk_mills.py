"""Catalog jobs for disk_mills."""

from src.tool_updater.classes.tool_classes.milling.disk_mill import (
    DiskOtreznoiChamfer,
    DiskOtreznoiFlat,
    DiskOtreznoiRounding,
)
from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def disk_mills() -> list[GenerationJob]:
    """Build jobs for the disk_mills group."""
    jobs: list[GenerationJob] = []
    jobs.append(
        GenerationJob(
            tool_class=DiskOtreznoiFlat,
            target_path=OUTPUT_DIR / 'DiskOtreznoi' / 'Iscar SGSF-GSFN',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='disk_',
            file_name_suffix='_SGSF_GSFN',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'otrez_disk'
            / 'Iscar GSFN'
            / 'SGSF_GSFN.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'otrez_disk'
            / 'Iscar GSFN'
            / 'SGSF_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=DiskOtreznoiChamfer,
            target_path=OUTPUT_DIR
            / 'DiskOtreznoi'
            / 'Iscar SGSF-E8 GSFP-5.4-90',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='disk_',
            file_name_suffix='_SGSF_GSFP',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'otrez_disk'
            / 'Iscar E8 GSFP-5.4-90'
            / 'SGSF_GSFP.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'otrez_disk'
            / 'Iscar E8 GSFP-5.4-90'
            / 'SGSF_cut_data.json',
        )
    )
    jobs.append(
        GenerationJob(
            tool_class=DiskOtreznoiRounding,
            target_path=OUTPUT_DIR / 'DiskOtreznoi' / 'Iscar SGSF-GSFU',
            teeth_num=1,
            debug_mode=0,
            file_name_prefix='disk_',
            file_name_suffix='_SGSF_GSFU',
            path_to_catalog_geometry=CATALOGS_DIR
            / 'milling'
            / 'otrez_disk'
            / 'Iscar GSFU'
            / 'SGSF_GSFU.json',
            path_to_catalog_cut_data=CATALOGS_DIR
            / 'milling'
            / 'otrez_disk'
            / 'Iscar GSFU'
            / 'SGSF_cut_data.json',
        )
    )
    return jobs
