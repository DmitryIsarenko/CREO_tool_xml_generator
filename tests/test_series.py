"""Check the operator workflow and preserve the legacy calculation path."""

import csv
from math import pi
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree

import pytest

from src.tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from src.tool_updater.series import (
    CUTTING_COLUMNS,
    DRILL_GEOMETRY_COLUMNS,
    GEOMETRY_COLUMNS,
    MATERIALS,
    SETTINGS_FILE,
    create_series,
    load_machining,
    load_series,
    prepare_tools,
    read_catalogs,
)
from src.tool_updater.series_cli import main, write_tools


@pytest.fixture
def series_root(tmp_path: Path) -> Path:
    """Create synthetic tables, never manufacturer machining data."""
    root = tmp_path / 'catalogs'
    directory = create_series(root, 'sample')
    (directory / 'series.toml').write_text(
        'name = "Учебная серия"\ntype = "ballmill"\nteeth = 2\n',
        encoding='utf-8',
    )
    (directory / 'geometry.csv').write_text(
        ';'.join(GEOMETRY_COLUMNS) + '\n6;12;60;A & B\n',
        encoding='utf-8-sig',
    )
    with (directory / 'cutting.csv').open(
        'w', encoding='utf-8-sig', newline=''
    ) as stream:
        writer = csv.writer(stream, delimiter=';')
        writer.writerow(CUTTING_COLUMNS)
        writer.writerows(
            (material, '6', '100', 'F', '300') for material in MATERIALS
        )
    return root


def test_operator_workflow(
    series_root: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """List, inspect, check and generate a series without changing Python."""
    args = ['--catalogs', str(series_root)]
    assert main([*args, 'types']) == 0
    assert main([*args, 'list']) == 0
    assert 'Учебная серия' in capsys.readouterr().out
    assert main([*args, 'check', '--series', 'sample']) == 0
    assert main([*args, 'show', '--series', 'sample']) == 0
    assert 'F=180.0' in capsys.readouterr().out
    output = tmp_path / 'xml'
    assert not output.exists()
    generate = [
        *args,
        'generate',
        '--series',
        'sample',
        '--output',
        str(output),
    ]
    assert main(generate) == 0
    files = list(output.glob('*.xml'))
    assert len(files) == 1
    root = ElementTree.parse(files[0]).getroot()
    comment = root.find('.//MfgParam[@Name="TOOL_COMMENT"]')
    assert comment is not None and comment.get('Value') == 'A & B'
    original = files[0].read_bytes()
    assert main(generate) == 1
    assert files[0].read_bytes() == original
    assert main([*generate, '--overwrite']) == 0


@pytest.mark.parametrize('kind', ['F', 'Fz', 'Fn'])
def test_feed_units(series_root: Path, kind: str) -> None:
    """Normalize explicit feed units before applying mode multipliers."""
    directory = series_root / 'sample'
    value = {'F': 300, 'Fz': 0.03, 'Fn': 0.06}[kind]
    (directory / 'cutting.csv').write_text(
        ';'.join(CUTTING_COLUMNS)
        + '\n'
        + ''.join(
            f'{material};6;100;{kind};{value}\n' for material in MATERIALS
        ),
        encoding='utf-8',
    )
    tools = prepare_tools(
        load_series(series_root, 'sample'), load_machining(SETTINGS_FILE)
    )
    expected = 300 if kind == 'F' else 0.06 * 1000 * 100 / (pi * 6)
    parameters = tools[0].tool_data['cut_data']['iso_P']['roughing']
    assert parameters['TOOL_FEED_RATE'] == round(expected * 0.6, 3)


@pytest.mark.parametrize(
    ('file', 'content', 'message'),
    [
        ('geometry.csv', 'bad header\n', 'заголовок'),
        ('geometry.csv', ';'.join(GEOMETRY_COLUMNS) + '\n', 'хотя бы'),
        (
            'geometry.csv',
            ';'.join(GEOMETRY_COLUMNS) + '\n6;70;60;x\n',
            'длина',
        ),
        (
            'geometry.csv',
            ';'.join(GEOMETRY_COLUMNS) + '\nNaN;12;60;x\n',
            'конечным',
        ),
        (
            'geometry.csv',
            ';'.join(GEOMETRY_COLUMNS) + '\n6.001;12;60;x\n',
            'двух',
        ),
        (
            'geometry.csv',
            ';'.join(GEOMETRY_COLUMNS) + '\n6;12;60;x\n6;12;60;y\n',
            'повторно',
        ),
        (
            'cutting.csv',
            ';'.join(CUTTING_COLUMNS) + '\niso_P;6;100;F;300\n',
            'нет групп',
        ),
        (
            'cutting.csv',
            ';'.join(CUTTING_COLUMNS) + '\niso_P;6;100;bad;300\n',
            'feed_kind',
        ),
        (
            'cutting.csv',
            ';'.join(CUTTING_COLUMNS) + '\niso_P;6;100;F;0\n',
            'больше нуля',
        ),
    ],
)
def test_bad_tables(
    series_root: Path, file: str, content: str, message: str
) -> None:
    """Reject invalid tables with a source path and a useful reason."""
    path = series_root / 'sample' / file
    path.write_text(content, encoding='utf-8')
    with pytest.raises(ValueError, match=message) as error:
        read_catalogs(load_series(series_root, 'sample'))
    assert str(path) in str(error.value)


def test_new_template_requires_configuration(tmp_path: Path) -> None:
    """Do not silently assume the number of teeth in a new series."""
    assert main(['--catalogs', str(tmp_path), 'init', '--series', 'new']) == 0
    assert main(['--catalogs', str(tmp_path), 'check', '--series', 'new']) == 1
    assert main(['--catalogs', str(tmp_path), 'init', '--series', 'new']) == 1
    assert (
        main(['--catalogs', str(tmp_path), 'init', '--series', '../bad']) == 1
    )


def test_legacy_defaults_unchanged(series_root: Path) -> None:
    """Keep user settings isolated from legacy class attributes."""
    before = {
        key: value.copy()
        for key, value in BallMill.finishing_roughing_options.items()
    }
    machining = load_machining(SETTINGS_FILE)
    machining.modes['roughing']['feed_rate_multiplier'] = 0.2
    tools = prepare_tools(load_series(series_root, 'sample'), machining)
    assert (
        tools[0].tool_data['cut_data']['iso_P']['roughing']['TOOL_FEED_RATE']
        == 60
    )
    assert BallMill.finishing_roughing_options == before


def test_write_failure_preserves_previous_file(
    series_root: Path, tmp_path: Path
) -> None:
    """Remove incomplete temporary output and keep the previous XML."""
    tools = prepare_tools(
        load_series(series_root, 'sample'), load_machining(SETTINGS_FILE)
    )
    output = tmp_path / 'output'
    write_tools(tools, output, overwrite=False)
    target = next(output.glob('*.xml'))
    previous = target.read_bytes()
    with patch.object(Path, 'replace', side_effect=OSError('disk failure')):
        with pytest.raises(OSError, match='disk failure'):
            write_tools(tools, output, overwrite=True)
    assert target.read_bytes() == previous
    assert list(output.iterdir()) == [target]


def test_settings_reject_unknown_keys(tmp_path: Path) -> None:
    """Reject misspelled multiplier names instead of ignoring them."""
    settings = tmp_path / 'machining.toml'
    settings.write_text(
        SETTINGS_FILE.read_text(encoding='utf-8').replace(
            'feed_multiplier', 'feed_multipler'
        ),
        encoding='utf-8',
    )
    with pytest.raises(ValueError, match='нужны поля'):
        load_machining(settings)


def test_multiple_diameters_keep_independent_speeds(series_root: Path) -> None:
    """Keep decimal diameters and per-size cutting speeds independent."""
    directory = series_root / 'sample'
    (directory / 'geometry.csv').write_text(
        ';'.join(GEOMETRY_COLUMNS) + '\n6,01;12;60;first\n6,1;12;60;second\n',
        encoding='utf-8',
    )
    (directory / 'cutting.csv').write_text(
        ';'.join(CUTTING_COLUMNS)
        + '\n'
        + ''.join(
            f'{material};{diameter};{speed};F;300\n'
            for diameter, speed in [('6,01', 100), ('6,1', 200)]
            for material in MATERIALS
        ),
        encoding='utf-8',
    )
    tools = prepare_tools(
        load_series(series_root, 'sample'), load_machining(SETTINGS_FILE)
    )
    assert len(tools) == 2
    assert len({tool.tool_data['tool_name_for_xml'] for tool in tools}) == 2
    assert [
        tool.tool_data['cut_data']['iso_P']['roughing']['TOOL_SURFACE_SPEED']
        for tool in tools
    ] == [100, 200]


def test_publication_race_does_not_replace_file(
    series_root: Path, tmp_path: Path
) -> None:
    """Refuse a concurrent collision and remove the temporary file."""
    tools = prepare_tools(
        load_series(series_root, 'sample'), load_machining(SETTINGS_FILE)
    )
    output = tmp_path / 'output'

    def concurrent_write(source: Path, target: Path) -> None:
        target.write_bytes(b'concurrent output')
        raise FileExistsError(target)

    with patch('src.tool_updater.series_cli.os.link', concurrent_write):
        with pytest.raises(FileExistsError):
            write_tools(tools, output, overwrite=False)
    files = list(output.iterdir())
    assert len(files) == 1
    assert files[0].read_bytes() == b'concurrent output'


def test_default_settings_preserve_legacy_calculations(
    series_root: Path,
) -> None:
    """Match the existing BallMill calculations with default settings."""
    series = load_series(series_root, 'sample')
    geometry, cutting = read_catalogs(series)
    legacy = BallMill(
        tool_size_from_geom_catalogue='6.00',
        catalog_tool_geometry=geometry,
        catalog_tool_cut_data=cutting['6.00'],
        teeth_num=2,
        file_name_prefix='sample_',
        file_name_suffix='',
        debug_mode=0,
    )
    tool = prepare_tools(series, load_machining(SETTINGS_FILE))[0]
    assert tool.tool_data['cut_data'] == legacy.tool_data['cut_data']
    assert tool.tool_data['LENGTH'] == legacy.tool_data['LENGTH']


@pytest.mark.parametrize(
    ('tool_type', 'geometry_columns', 'geometry_row', 'xml_parameter'),
    [
        (
            'drill',
            DRILL_GEOMETRY_COLUMNS,
            '6;20;70;DRILL & TEST;135',
            'POINT_ANGLE',
        ),
        (
            'endmill',
            GEOMETRY_COLUMNS,
            '6;20;70;ENDMILL & TEST',
            'NUM_OF_TEETH',
        ),
    ],
)
def test_drill_and_endmill_workflows(
    tmp_path: Path,
    tool_type: str,
    geometry_columns: tuple[str, ...],
    geometry_row: str,
    xml_parameter: str,
) -> None:
    """Create each new type with its own table and default settings."""
    root = tmp_path / 'catalogs'
    directory = create_series(root, tool_type, tool_type)
    (directory / 'series.toml').write_text(
        f'name = "{tool_type}"\ntype = "{tool_type}"\nteeth = 2\n',
        encoding='utf-8',
    )
    (directory / 'geometry.csv').write_text(
        ';'.join(geometry_columns) + f'\n{geometry_row}\n',
        encoding='utf-8',
    )
    (directory / 'cutting.csv').write_text(
        ';'.join(CUTTING_COLUMNS)
        + '\n'
        + ''.join(f'{material};6;100;F;300\n' for material in MATERIALS),
        encoding='utf-8',
    )
    series = load_series(root, tool_type)
    tools = prepare_tools(series, load_machining(series_settings(tool_type)))
    assert len(tools) == 1
    tools[0].set_tool_xml()
    root_xml = ElementTree.fromstring(tools[0].tool_xml)
    parameter = root_xml.find(f'.//MfgParam[@Name="{xml_parameter}"]')
    assert parameter is not None
    if tool_type == 'drill':
        assert parameter.get('Value') == '135.0'
        assert (
            tools[0].tool_data['cut_data']['iso_P']['roughing'][
                'TOOL_RADIAL_DEPTH'
            ]
            == 0
        )


def series_settings(tool_type: str) -> Path:
    """Return the default settings file for one user series type."""
    from src.tool_updater.series import SETTINGS_FILES

    return SETTINGS_FILES[tool_type]


def test_drill_requires_point_angle(tmp_path: Path) -> None:
    """Reject a drill table that uses the generic geometry header."""
    root = tmp_path / 'catalogs'
    directory = create_series(root, 'drill', 'drill')
    (directory / 'series.toml').write_text(
        'name = "Drill"\ntype = "drill"\nteeth = 2\n', encoding='utf-8'
    )
    (directory / 'geometry.csv').write_text(
        ';'.join(GEOMETRY_COLUMNS) + '\n6;20;70;test\n', encoding='utf-8'
    )
    with pytest.raises(ValueError, match='point_angle_deg'):
        read_catalogs(load_series(root, 'drill'))
