"""Copy tool XML with new identifiers without deleting source files."""

import argparse
from collections.abc import Sequence
from pathlib import Path
from xml.etree import ElementTree

from src.tool_updater.config import TEXT_ENCODING, XML_EXTENSION


def execute_renaming(
    path_from: str | Path,
    path_to: str | Path,
    *,
    prefix: str = '',
    suffix: str = '_B',
    new_register: str = '2',
    overwrite: bool = False,
    dry_run: bool = True,
) -> list[tuple[Path, Path]]:
    """Validate XML copies and optionally write them to another directory."""
    source = Path(path_from).resolve()
    target = Path(path_to).resolve()
    if source == target:
        raise ValueError('Source and target directories must differ.')
    if not source.is_dir():
        raise NotADirectoryError(source)
    if not new_register.isdecimal():
        raise ValueError('Register must be a non-negative integer.')
    for part in (prefix, suffix):
        if any(char in part for char in '/\\:*?"<>|'):
            raise ValueError('Prefix and suffix must be filename fragments.')

    plans: list[tuple[Path, Path]] = []
    documents: list[ElementTree.ElementTree[ElementTree.Element[str]]] = []
    names: set[str] = set()
    source_files = [
        file
        for file in sorted(source.iterdir())
        if file.is_file() and file.suffix.lower() == XML_EXTENSION
    ]
    for file in source_files:
        destination = target / f'{prefix}{file.stem}{suffix}{file.suffix}'
        name = destination.name.casefold()
        if name in names:
            raise ValueError(f'Duplicate output filename: {destination}')
        names.add(name)
        if destination.exists() and not overwrite:
            raise FileExistsError(destination)
        if destination.is_dir():
            raise IsADirectoryError(destination)
        if destination.is_symlink():
            raise ValueError(
                f'Symbolic-link output is not allowed: {destination}'
            )
        if any(destination == original for original in source_files):
            raise ValueError('A destination points to a source XML.')

        tree = ElementTree.parse(file)
        tools = list(tree.getroot().iter('Tool'))
        if not tools:
            raise ValueError(f'No Tool element in {file}')
        for tool in tools:
            identifier = tool.get('Id')
            if not identifier:
                raise ValueError(f'Missing Tool Id in {file}')
            tool.set('Id', f'{prefix}{identifier}{suffix}')
        for element in tree.getroot().iter():
            if 'Register' in element.attrib:
                element.set('Register', new_register)
        plans.append((file, destination))
        documents.append(tree)

    if not dry_run and plans:
        target.mkdir(parents=True, exist_ok=True)
        mode = 'wb' if overwrite else 'xb'
        for (_, destination), tree in zip(plans, documents, strict=True):
            with destination.open(mode) as output:
                tree.write(
                    output, encoding=TEXT_ENCODING, xml_declaration=True
                )
    return plans


def main(argv: Sequence[str] | None = None) -> int:
    """Preview XML copies unless writing is explicitly requested."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('target', type=Path)
    parser.add_argument('--prefix', default='')
    parser.add_argument('--suffix', default='_B')
    parser.add_argument('--register', default='2')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args(argv)
    try:
        plans = execute_renaming(
            args.source,
            args.target,
            prefix=args.prefix,
            suffix=args.suffix,
            new_register=args.register,
            overwrite=args.overwrite,
            dry_run=not args.write,
        )
    except (OSError, ValueError, ElementTree.ParseError) as exc:
        parser.exit(1, f'Copy failed: {exc}\n')
    for source, target in plans:
        print(f'{source} -> {target}')
    print(
        f'{len(plans)} files; ' + ('written' if args.write else 'preview only')
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
