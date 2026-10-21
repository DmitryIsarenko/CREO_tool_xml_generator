"""Command-line entry point for catalog generation."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from src import configure_logging
from src.tool_updater.config import OUTPUT_DIR
from src.tool_updater.jobs import JOB_BUILDERS
from src.tool_updater.runner import run_jobs


def main(argv: Sequence[str] | None = None) -> int:
    """Select a catalog group and run its jobs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List job groups')
    parser.add_argument('--group', choices=sorted(JOB_BUILDERS))
    parser.add_argument('--output', type=Path, default=OUTPUT_DIR)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args(argv)
    if args.list:
        print('\n'.join(sorted(JOB_BUILDERS)))
        return 0
    if args.group is None:
        parser.print_help()
        return 0
    configure_logging()
    try:
        run_jobs(
            JOB_BUILDERS[args.group](),
            output_directory=args.output.resolve(),
            overwrite=args.overwrite,
        )
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Generation failed: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
