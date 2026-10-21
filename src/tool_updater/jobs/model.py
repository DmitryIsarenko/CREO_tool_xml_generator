"""Typed descriptions of catalog generation jobs."""

from dataclasses import dataclass
from pathlib import Path

from src.tool_updater.classes.tool_classes.base_tool import BaseTool


@dataclass(frozen=True, kw_only=True)
class GenerationJob:
    """Describe one catalog series without running the generator."""

    tool_class: type[BaseTool]
    path_to_catalog_geometry: Path
    path_to_catalog_cut_data: Path
    teeth_num: int
    target_path: Path
    file_name_prefix: str
    file_name_suffix: str
    debug_mode: int = 0
