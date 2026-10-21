import json
from pathlib import Path

from src.tool_updater.classes.tool_classes.base_tool import BaseTool


class ToolGenerator:
    """Generate tool XML files from geometry and cutting data catalogs."""

    @staticmethod
    def create_tools(*,
                     tool_class: type[BaseTool],
                     path_to_catalog_geometry: str | Path,
                     path_to_catalog_cut_data: str | Path,
                     teeth_num: int,
                     target_path: str | Path,
                     file_name_prefix: str,
                     file_name_suffix: str,
                     debug_mode: int,
                     ) -> None:
        """Read catalogs and write XML files to the target directory."""
        with Path(path_to_catalog_geometry).open(encoding='utf-8') as f:
            catalog_tool_geometry = json.load(f)
        with Path(path_to_catalog_cut_data).open(encoding='utf-8') as f:
            catalog_tool_cut_data = json.load(f)

        list_of_tool_sizes = [tool_size for tool_size in catalog_tool_geometry.keys()]
        list_of_new_tool_obj = list()

        for tool_size in list_of_tool_sizes:
            tool = tool_class(
                tool_size_from_geom_catalogue=tool_size,
                catalog_tool_cut_data=catalog_tool_cut_data,
                catalog_tool_geometry=catalog_tool_geometry,
                teeth_num=teeth_num,
                file_name_prefix=file_name_prefix,
                file_name_suffix=file_name_suffix,
                debug_mode=debug_mode,
            )
            list_of_new_tool_obj.append(tool)

        for t in list_of_new_tool_obj:
            print(t.tool_data["tool_name_str"])

        target_directory = Path(target_path)
        target_directory.mkdir(parents=True, exist_ok=True)

        for tool in list_of_new_tool_obj:
            tool.set_tool_xml()
            tool.write_new_file(path=target_directory)
