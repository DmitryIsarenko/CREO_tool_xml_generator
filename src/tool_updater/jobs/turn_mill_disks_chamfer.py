"""Catalog jobs for turn_mill_disks_chamfer."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_DISKS_CHAMFER_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_disks_chamfer() -> list[GenerationJob]:
    """Build jobs for the turn_mill_disks_chamfer group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_DISKS_CHAMFER_HOLDERS
    for holder in all_holders:
        holder_subdir = all_holders[holder]['holder_subdir']
        tool_class = all_holders[holder]['tool_class']
        tool_prefix = holder_subdir.lower() + '_'
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'DiskOtreznoi'
                / 'Iscar SGSF-E8 GSFP-5.4-90',
                teeth_num=1,
                debug_mode=0,
                file_name_prefix=tool_prefix + 'disk_',
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
    return jobs
