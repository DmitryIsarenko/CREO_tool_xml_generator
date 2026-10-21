"""Catalog jobs for turn_mill_disks."""

from src.tool_updater.jobs.model import GenerationJob
from src.tool_updater.jobs.turn_mill_disks_chamfer import (
    turn_mill_disks_chamfer,
)
from src.tool_updater.jobs.turn_mill_disks_flat import turn_mill_disks_flat
from src.tool_updater.jobs.turn_mill_disks_rounding import (
    turn_mill_disks_rounding,
)


def turn_mill_disks() -> list[GenerationJob]:
    """Build jobs for the turn_mill_disks group."""
    jobs: list[GenerationJob] = []
    jobs.extend(turn_mill_disks_flat())
    jobs.extend(turn_mill_disks_chamfer())
    jobs.extend(turn_mill_disks_rounding())
    return jobs
