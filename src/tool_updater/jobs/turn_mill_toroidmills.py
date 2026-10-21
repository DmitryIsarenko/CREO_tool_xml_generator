"""Catalog jobs for turn_mill_toroidmills."""

from src.tool_updater.config import CATALOGS_DIR, OUTPUT_DIR
from src.tool_updater.holders import TURN_MILL_TOROIDMILLS_HOLDERS
from src.tool_updater.jobs.model import GenerationJob


def turn_mill_toroidmills() -> list[GenerationJob]:
    """Build jobs for the turn_mill_toroidmills group."""
    jobs: list[GenerationJob] = []
    all_holders = TURN_MILL_TOROIDMILLS_HOLDERS
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
                / 'ToroidMill'
                / 'Gesac UA100-R3',
                debug_mode=0,
                file_name_prefix=tool_prefix + 'fr_tor_',
                teeth_num=3,
                file_name_suffix='_UA100-R3',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'toroidal_endmills'
                / 'Gesac'
                / 'isoN'
                / 'UA100-R3'
                / 'UA100-R3.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'toroidal_endmills'
                / 'Gesac'
                / 'isoN'
                / 'UA100-R3'
                / 'UA100-R3_cut_data.json',
            )
        )
        jobs.append(
            GenerationJob(
                tool_class=tool_class,
                target_path=OUTPUT_DIR
                / 'TurnMill'
                / holder_subdir
                / 'ToroidMill'
                / 'Gesac SS600-R4',
                debug_mode=0,
                file_name_prefix=tool_prefix + 'fr_tor_',
                teeth_num=4,
                file_name_suffix='_SS600-R4',
                path_to_catalog_geometry=CATALOGS_DIR
                / 'milling'
                / 'toroidal_endmills'
                / 'Gesac'
                / 'isoP_isoM'
                / 'SS600-R4'
                / 'SS600-R4.json',
                path_to_catalog_cut_data=CATALOGS_DIR
                / 'milling'
                / 'toroidal_endmills'
                / 'Gesac'
                / 'isoP_isoM'
                / 'SS600-R4'
                / 'SS600-R4_cut_data.json',
            )
        )
    return jobs
