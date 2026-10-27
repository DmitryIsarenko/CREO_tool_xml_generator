"""Provide the operator workflow for user-managed series."""

import argparse
from collections.abc import Sequence
import os
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile

from src.tool_updater.classes.tool_classes.base_tool import BaseTool
from src.tool_updater.config import MAX_RPM, OUTPUT_DIR
from src.tool_updater.series import (
    SERIES_DIR,
    SERIES_TYPES,
    SETTINGS_FILES,
    create_series,
    load_machining,
    load_series,
    prepare_tools,
)


def write_tools(
    tools: list[BaseTool], directory: Path, *, overwrite: bool
) -> None:
    """Publish complete files without truncating existing output."""
    targets = [
        directory / f'{tool.tool_data["file_name"]}.xml' for tool in tools
    ]
    for target in targets:
        if target.is_symlink() or target.is_dir():
            raise ValueError(f'{target}: нельзя заменить папку или ссылку.')
        if target.exists() and not overwrite:
            raise FileExistsError(f'{target}: для замены нужен --overwrite.')
    directory.mkdir(parents=True, exist_ok=True)
    for tool, target in zip(tools, targets, strict=True):
        temporary: Path | None = None
        try:
            with NamedTemporaryFile(
                mode='w', encoding='utf-8', dir=directory, delete=False
            ) as stream:
                temporary = Path(stream.name)
                stream.write(tool.tool_xml)
            if overwrite:
                temporary.replace(target)
            else:
                # A hard link publishes a complete file and refuses collisions.
                os.link(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


def _print_tools(tools: list[BaseTool]) -> None:
    for tool in tools:
        data = tool.tool_data
        print(f'\n{data["file_name"]}.xml')
        print(
            f'  Диаметр: {data["CUTTER_DIAM"]} мм; '
            f'зубьев: {data["NUM_OF_TEETH"]}'
        )
        for material in ('iso_P', 'iso_M', 'iso_K', 'iso_N', 'iso_S', 'iso_H'):
            for mode, label in (
                ('roughing', 'черновая'),
                ('finishing', 'чистовая'),
            ):
                parameters = data['cut_data'][material][mode]
                print(
                    f'  {material}, {label}: '
                    f'Vc={parameters["TOOL_SURFACE_SPEED"]} м/мин; '
                    f'n={parameters["TOOL_SPINDLE_RPM"]} об/мин; '
                    f'F={parameters["TOOL_FEED_RATE"]} мм/мин; '
                    f'Ap={parameters["TOOL_AXIAL_DEPTH"]} мм; '
                    f'Ae={parameters["TOOL_RADIAL_DEPTH"]} мм'
                )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the series CLI and report expected errors without tracebacks."""
    parser = argparse.ArgumentParser(
        description='Добавление серий инструмента без редактирования Python.'
    )
    parser.add_argument(
        '--catalogs',
        type=Path,
        default=SERIES_DIR,
        help='папка серий (по умолчанию catalogs в проекте)',
    )
    commands = parser.add_subparsers(dest='command', title='команды')
    commands.add_parser('types', help='поддерживаемые типы инструмента')
    commands.add_parser('list', help='список серий, включая незаполненные')
    init = commands.add_parser('init', help='создать пустые таблицы серии')
    init.add_argument(
        '--series', required=True, help='имя папки, например gesac_b2'
    )
    init.add_argument(
        '--type',
        choices=SERIES_TYPES,
        default='ballmill',
        help='тип инструмента',
    )
    for command, help_text in (
        ('show', 'показать настройки и рассчитанные режимы без записи'),
        ('check', 'проверить таблицы, расчёты и XML без записи'),
        ('generate', 'создать XML выбранной серии'),
    ):
        subparser = commands.add_parser(command, help=help_text)
        subparser.add_argument(
            '--series', required=True, help='имя папки серии'
        )
        subparser.add_argument(
            '--settings',
            type=Path,
            help='файл множителей; по умолчанию — для типа серии',
        )
        if command == 'generate':
            subparser.add_argument(
                '--output', type=Path, help='итоговая папка XML'
            )
            subparser.add_argument(
                '--overwrite', action='store_true', help='разрешить замену XML'
            )
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    try:
        if args.command == 'types':
            print('ballmill — сферическая фреза, стандартная сборка')
            print('countersink — зенковка, стандартная сборка')
            print('drill — спиральное сверло, стандартная сборка')
            print('endmill — концевая фреза, стандартная сборка')
        elif args.command == 'init':
            directory = create_series(args.catalogs, args.series, args.type)
            print(
                f'Создано: {directory}\n'
                'Заполните series.toml, geometry.csv, cutting.csv, source.txt.'
            )
        elif args.command == 'list':
            invalid = False
            paths = sorted(args.catalogs.glob('*/series.toml'))
            if not paths:
                print('Серий нет. Создайте серию командой init.')
            for path in paths:
                try:
                    series = load_series(args.catalogs, path.parent.name)
                    print(
                        f'{series.identifier} — {series.name} '
                        f'({series.teeth} зубьев)'
                    )
                except (OSError, ValueError) as exc:
                    invalid = True
                    print(f'{path.parent.name} — ошибка описания: {exc}')
            print('Список не подтверждает готовность таблиц. Выполните check.')
            return 1 if invalid else 0
        else:
            series = load_series(args.catalogs, args.series)
            settings = args.settings or SETTINGS_FILES[series.tool_type]
            machining = load_machining(settings)
            tools = prepare_tools(series, machining)
            print(f'{series.name}: проверено инструментов — {len(tools)}.')
            if args.command == 'show':
                print(f'Настройки: {settings.resolve()}')
                print(f'Множители: {machining.modes}')
                print(f'Коэффициенты Ap: {machining.axial}')
                print(f'Коэффициенты Ae: {machining.radial}')
                print(f'Предел оборотов старого расчёта: {MAX_RPM} об/мин.')
                _print_tools(tools)
            elif args.command == 'generate':
                output = (
                    args.output or OUTPUT_DIR / 'series' / series.identifier
                )
                write_tools(tools, output, overwrite=args.overwrite)
                print(f'XML записаны: {output.resolve()}')
            print(
                'Проверьте режимы, сборку и импорт в CREO '
                'до применения на станке.'
            )
    except (OSError, ValueError) as exc:
        print(f'Ошибка: {exc}', file=sys.stderr)
        return 1
    return 0
