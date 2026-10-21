"""Execute typed catalog jobs."""

from collections.abc import Iterable
from pathlib import Path

from src.tool_updater.classes.tool_generator import ToolGenerator
from src.tool_updater.config import OUTPUT_DIR
from src.tool_updater.jobs.model import GenerationJob


def run_jobs(
    jobs: Iterable[GenerationJob],
    *,
    output_directory: Path = OUTPUT_DIR,
    overwrite: bool = False,
) -> None:
    """Execute jobs with an explicit replacement policy."""
    for job in jobs:
        relative_target = job.target_path.relative_to(OUTPUT_DIR)
        ToolGenerator.create_tools(
            tool_class=job.tool_class,
            path_to_catalog_geometry=job.path_to_catalog_geometry,
            path_to_catalog_cut_data=job.path_to_catalog_cut_data,
            teeth_num=job.teeth_num,
            target_path=output_directory / relative_target,
            file_name_prefix=job.file_name_prefix,
            file_name_suffix=job.file_name_suffix,
            debug_mode=job.debug_mode,
            overwrite=overwrite,
        )
