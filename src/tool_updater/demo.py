"""Generate one synthetic example, not for machining."""

from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

from src import configure_logging
from src.tool_updater.classes.tool_classes.milling.sphere_mill import (
    BallMill,
)
from src.tool_updater.classes.tool_generator import ToolGenerator
from src.tool_updater.config import PROJECT_DIR


def main() -> None:
    """Generate and check demo XML without using production output paths."""
    configure_logging()
    example_directory = PROJECT_DIR / 'examples' / 'demo'
    output_directory = PROJECT_DIR / 'generated_xmls' / 'demo'
    output_directory.mkdir(parents=True, exist_ok=True)

    # Validate the new XML before replacing the previous demo result.
    with TemporaryDirectory(dir=output_directory) as temporary_directory:
        ToolGenerator.create_tools(
            tool_class=BallMill,
            path_to_catalog_geometry=example_directory / 'geometry.json',
            path_to_catalog_cut_data=example_directory / 'cut_data.json',
            teeth_num=2,
            target_path=Path(temporary_directory),
            file_name_prefix='demo_ball_',
            file_name_suffix='_NOT_FOR_MACHINING',
            debug_mode=0,
        )
        xml_files = list(Path(temporary_directory).glob('*.xml'))
        if len(xml_files) != 1:
            raise RuntimeError('Expected exactly one demo XML file.')
        xml_file = xml_files[0]
        ElementTree.parse(xml_file)
        output_file = output_directory / xml_file.name
        xml_file.replace(output_file)

    print(f'Demo XML: {output_file}')
    print('Synthetic data only. Do not use this XML for machining.')


if __name__ == '__main__':
    main()
