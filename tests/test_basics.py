"""Check basic calculations and non-destructive file operations."""

import json
from math import pi
from pathlib import Path
from xml.etree import ElementTree

import pytest

from src.tool_updater import config
from src.tool_updater.classes.tool_classes.milling.sphere_mill import BallMill
from src.tool_updater.classes.tool_generator import ToolGenerator
from src.tool_updater.classes.tool_renamer import execute_renaming
from src.tool_updater.classes.turnmill_len_adaptors import (
    adapt_flute_length,
    adapt_length,
)
from src.tool_updater.data_types import Catalog
from src.tool_updater.jobs import JOB_BUILDERS
from src.tool_updater.main import main


@pytest.fixture
def catalogs() -> tuple[Catalog, Catalog]:
    """Read the small synthetic catalogs shipped with the demo."""
    directory = config.PROJECT_DIR / 'examples' / 'demo'
    geometry = json.loads((directory / 'geometry.json').read_text())
    cutting = json.loads((directory / 'cut_data.json').read_text())
    return geometry, cutting


@pytest.fixture
def ballmill(catalogs: tuple[Catalog, Catalog]) -> BallMill:
    """Build one tool without writing files or configuring logging."""
    geometry, cutting = catalogs
    return BallMill(
        tool_size_from_geom_catalogue='6.00',
        catalog_tool_cut_data=cutting,
        catalog_tool_geometry=geometry,
        teeth_num=2,
        file_name_prefix='test_',
        file_name_suffix='',
        debug_mode=0,
    )


def _generate(
    target: Path,
    geometry: Path | None = None,
    *,
    overwrite: bool = False,
) -> None:
    directory = config.PROJECT_DIR / 'examples' / 'demo'
    ToolGenerator.create_tools(
        tool_class=BallMill,
        path_to_catalog_geometry=geometry or directory / 'geometry.json',
        path_to_catalog_cut_data=directory / 'cut_data.json',
        teeth_num=2,
        target_path=target,
        file_name_prefix='test_',
        file_name_suffix='',
        debug_mode=0,
        overwrite=overwrite,
    )


@pytest.mark.parametrize(
    ('length', 'expected'), [(60, 60), (86, 86), (100, 85.9)]
)
def test_holder_length_limit(length: float, expected: float) -> None:
    """Keep safe lengths and shorten lengths above the holder limit."""
    assert (
        adapt_length(
            default_full_length=length,
            max_safe_length=180,
            length_taken_by_holder=94,
        )
        == expected
    )


@pytest.mark.parametrize(('flute', 'expected'), [(12, 12), (60, 59), (65, 59)])
def test_flute_length_limit(flute: float, expected: float) -> None:
    """Keep the flute shorter than the adapted tool body."""
    assert (
        adapt_flute_length(default_flute_length=flute, full_length_adapted=60)
        == expected
    )


def test_ballmill_calculations(ballmill: BallMill) -> None:
    """Preserve diameter, speed, feed and engagement calculations."""
    assert ballmill.tool_data['tool_diam_float'] == 6
    assert ballmill.tool_data['NUM_OF_TEETH'] == 2
    assert ballmill.calc_rpm(100) == round(
        1000 * 100 / (pi * 6), config.NDIGITS_SPINDLE
    )
    roughing = ballmill.tool_data['cut_data']['iso_P']['roughing']
    assert roughing['TOOL_SURFACE_SPEED'] == 100
    assert roughing['TOOL_FEED_RATE'] == 180
    assert roughing['TOOL_AXIAL_DEPTH'] == 3
    assert roughing['TOOL_RADIAL_DEPTH'] == round(
        6 * 0.01875, config.NDIGITS_RADIAL_FEED
    )


def test_default_data_is_not_shared(
    ballmill: BallMill, catalogs: tuple[Catalog, Catalog]
) -> None:
    """Keep nested cutting data separate for each tool instance."""
    other = BallMill(
        tool_size_from_geom_catalogue='6.00',
        catalog_tool_geometry=catalogs[0],
        catalog_tool_cut_data=catalogs[1],
        teeth_num=2,
        file_name_prefix='',
        file_name_suffix='',
        debug_mode=0,
    )
    ballmill.tool_data['cut_data']['iso_P']['roughing']['TOOL_FEED_RATE'] = 999
    assert (
        other.tool_data['cut_data']['iso_P']['roughing']['TOOL_FEED_RATE']
        == 180
    )


def test_generation_and_overwrite(tmp_path: Path) -> None:
    """Write valid XML and replace existing output only when requested."""
    _generate(tmp_path)
    files = list(tmp_path.glob('*.xml'))
    assert len(files) == 1
    root = ElementTree.parse(files[0]).getroot()
    assert root.find('.//MfgParam[@Name="CUTTER_DIAM"]') is not None
    files[0].write_bytes(b'existing output')
    with pytest.raises(FileExistsError):
        _generate(tmp_path)
    assert files[0].read_bytes() == b'existing output'
    _generate(tmp_path, overwrite=True)
    ElementTree.parse(files[0])


def test_catalog_error_has_context(
    tmp_path: Path, catalogs: tuple[Catalog, Catalog]
) -> None:
    """Report the tool size and source path before creating output."""
    geometry, _ = catalogs
    del geometry['6.00']['full_body_len']
    catalog = tmp_path / 'broken.json'
    catalog.write_text(json.dumps(geometry), encoding='utf-8')
    output = tmp_path / 'output'
    with pytest.raises(ValueError, match='BallMill, size') as error:
        _generate(output, catalog)
    assert str(catalog) in str(error.value)
    assert isinstance(error.value.__cause__, KeyError)
    assert not output.exists()


def test_renaming_preview_and_copy(tmp_path: Path) -> None:
    """Preview without writing and copy XML without changing its source."""
    source = tmp_path / 'source'
    target = tmp_path / 'target'
    source.mkdir()
    original = source / 'tool.with.dots.xml'
    content = b'<Root><Tool Id="TEST"><Offset Register="1"/></Tool></Root>'
    original.write_bytes(content)
    plans = execute_renaming(source, target)
    assert len(plans) == 1
    assert not target.exists()
    execute_renaming(source, target, dry_run=False)
    assert original.read_bytes() == content
    copied = ElementTree.parse(target / 'tool.with.dots_B.xml').getroot()
    tool = copied.find('Tool')
    offset = copied.find('.//Offset')
    assert tool is not None and tool.get('Id') == 'TEST_B'
    assert offset is not None and offset.get('Register') == '2'
    with pytest.raises(FileExistsError):
        execute_renaming(source, target, dry_run=False)


def test_invalid_xml_does_not_create_partial_output(tmp_path: Path) -> None:
    """Validate all source XML before writing the first copy."""
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'a.xml').write_text('<Root><Tool Id="A"/></Root>')
    (source / 'b.xml').write_text('<broken>')
    target = tmp_path / 'target'
    with pytest.raises(ElementTree.ParseError):
        execute_renaming(source, target, dry_run=False)
    assert not target.exists()


def test_job_inventory() -> None:
    """Keep the complete catalog job inventory and local output paths."""
    jobs = [job for builder in JOB_BUILDERS.values() for job in builder()]
    assert len(JOB_BUILDERS) == 37
    assert len(jobs) == 565
    for job in jobs:
        assert job.path_to_catalog_geometry.is_file()
        assert job.path_to_catalog_cut_data.is_file()
        assert job.target_path.is_relative_to(config.OUTPUT_DIR)


def test_cli_without_group_does_not_run_jobs(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Show help or groups without invoking production generation."""

    def reject_generation(*args: object, **kwargs: object) -> None:
        pytest.fail('Generation must not run without an explicit group.')

    monkeypatch.setattr('src.tool_updater.main.run_jobs', reject_generation)
    assert main([]) == 0
    assert 'usage:' in capsys.readouterr().out
    assert main(['--list']) == 0
    assert set(capsys.readouterr().out.splitlines()) == set(JOB_BUILDERS)
