import json
from math import isfinite
from pathlib import Path

from src.tool_updater.classes.tool_classes.base_tool import BaseTool
from src.tool_updater.config import TEXT_ENCODING


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
                     overwrite: bool = False,
                     ) -> None:
        """Read catalogs and write XML files to the target directory."""
        with Path(path_to_catalog_geometry).open(encoding=TEXT_ENCODING) as f:
            catalog_tool_geometry = json.load(f)
        with Path(path_to_catalog_cut_data).open(encoding=TEXT_ENCODING) as f:
            catalog_tool_cut_data = json.load(f)

        if not isinstance(catalog_tool_geometry, dict) or not catalog_tool_geometry:
            raise ValueError(f'Expected non-empty geometry: {path_to_catalog_geometry}')
        if not isinstance(catalog_tool_cut_data, dict) or not catalog_tool_cut_data:
            raise ValueError(f'Expected non-empty cutting data: {path_to_catalog_cut_data}')
        if isinstance(teeth_num, bool) or teeth_num <= 0:
            raise ValueError('The number of teeth must be positive.')

        tools: list[BaseTool] = []

        for tool_size in catalog_tool_geometry:
            try:
                tool = tool_class(
                    tool_size_from_geom_catalogue=tool_size,
                    catalog_tool_cut_data=catalog_tool_cut_data,
                    catalog_tool_geometry=catalog_tool_geometry,
                    teeth_num=teeth_num,
                    file_name_prefix=file_name_prefix,
                    file_name_suffix=file_name_suffix,
                    debug_mode=debug_mode,
                )
                for field in ('CUTTER_DIAM', 'LENGTH', 'FLUTE_LENGTH',
                              'NUM_OF_TEETH'):
                    value = float(tool.tool_data[field])
                    if not isfinite(value) or value <= 0:
                        raise ValueError(f'{field} must be finite and positive')
            except (KeyError, ValueError, TypeError, IndexError,
                    ZeroDivisionError) as exc:
                raise ValueError(
                    f'{tool_class.__name__}, size {tool_size!r}: {exc}; '
                    f'geometry={path_to_catalog_geometry}; '
                    f'cutting data={path_to_catalog_cut_data}'
                ) from exc
            tools.append(tool)

        for tool in tools:
            print(tool.tool_data['tool_name_str'])

        target_directory = Path(target_path)
        names: set[str] = set()
        for tool in tools:
            name = (
                f'{tool.tool_data["file_name"]}{tool.tool_file_extension}'
            )
            if '/' in name or '\\' in name or Path(name).name != name:
                raise ValueError(f'Invalid output filename: {name!r}')
            normalized = name.casefold()
            if normalized in names:
                raise ValueError(f'Duplicate output filename: {name}')
            names.add(normalized)
            output_file = target_directory / name
            if output_file.exists() and not overwrite:
                raise FileExistsError(
                    f'{output_file}: use overwrite=True to replace it'
                )
            if output_file.is_dir():
                raise IsADirectoryError(output_file)
            tool.set_tool_xml()

        target_directory.mkdir(parents=True, exist_ok=True)
        for tool in tools:
            tool.write_new_file(path=target_directory, overwrite=overwrite)
