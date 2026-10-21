"""Generate one synthetic example on Windows, not for machining."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

from src import configure_logging
from src.tool_updater.classes.tool_classes.milling.sphere_mill import (
    BallMill,
)
from src.tool_updater.classes.tool_generator import ToolGenerator


def main() -> None:
    """Generate and check demo XML without using production output paths."""
    if os.name != 'nt':
        raise RuntimeError('The existing XML writer requires Windows.')

    configure_logging()
    project_directory = Path(__file__).resolve().parents[2]
    example_directory = project_directory / 'examples' / 'demo'
    output_directory = project_directory / 'generated_xmls' / 'demo'
    output_directory.mkdir(parents=True, exist_ok=True)

    # A fresh directory prevents an old XML from hiding a write failure.
    with TemporaryDirectory(dir=output_directory) as temporary_directory:
        ToolGenerator.create_tools(
            tool_class=BallMill,
            path_to_catalog_geometry=str(example_directory / 'geometry.json'),
            path_to_catalog_cut_data=str(example_directory / 'cut_data.json'),
            teeth_num=2,
            target_path=temporary_directory,
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