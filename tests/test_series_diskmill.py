import csv
from pathlib import Path
from xml.etree import ElementTree

from src.tool_updater.series import (
    DISKMILL_CUTTING_COLUMNS,
    DISKMILL_GEOMETRY_COLUMNS,
    MATERIALS,
    create_series,
    load_machining,
    load_series,
    prepare_tools,
)


def test_diskmill_series(
    tmp_path: Path,
) -> None:
    """Build a disk mill from CSV and verify its XML parameters."""
    root = tmp_path / 'catalogs'
    directory = create_series(root, 'disk', 'diskmill')
    (directory / 'series.toml').write_text(
        'name = "Disk"\ntype = "diskmill"\nteeth = 6\n',
        encoding='utf-8',
    )
    (directory / 'geometry.csv').write_text(
        ';'.join(DISKMILL_GEOMETRY_COLUMNS)
        + '\n100;5.4;0;0;0;20;110;25;22;6;DISK TEST\n',
        encoding='utf-8',
    )
    cutting_rows = [
        (material, '100', '120', 'Fz', '0.05', '5') for material in MATERIALS
    ]
    with (directory / 'cutting.csv').open(
        'w', encoding='utf-8', newline=''
    ) as stream:
        writer = csv.writer(stream, delimiter=';')
        writer.writerow(DISKMILL_CUTTING_COLUMNS)
        for row in cutting_rows:
            writer.writerow(row)
    series = load_series(root, 'disk')
    tools = prepare_tools(
        series, load_machining(Path('settings/diskmill.toml'))
    )
    assert len(tools) == 1
    xml = ElementTree.fromstring(tools[0].tool_xml)
    parameters = {
        node.get('Name'): node.get('Value')
        for node in xml.findall('.//MfgParam')
        if node.get('Name')
    }
    assert parameters['CUTTER_WIDTH'] == '5.4'
    assert parameters['SHANK_DIAM'] == '22.0'
    assert parameters['HOLDER_LEN'] == '110.0'
    assert (
        tools[0].tool_data['cut_data']['iso_P']['roughing'][
            'TOOL_FEED_PER_UNIT'
        ]
        == 0.05
    )
    assert (
        tools[0].tool_data['cut_data']['iso_P']['roughing'][
            'TOOL_RADIAL_DEPTH'
        ]
        == 5.0
    )
    assert 'Value="5.0"' in tools[0].tool_xml
    components = xml.findall('.//BOMComponent')
    assert len(components) == 5
    assert components[-1].get('Type') == 'GENERAL'
