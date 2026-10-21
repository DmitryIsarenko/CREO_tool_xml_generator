"""Catalog jobs for turn_mill_gribkovie."""

from src.tool_updater.jobs.model import GenerationJob
from src.tool_updater.jobs.turn_mill_gribkovie_chamfer import (
    turn_mill_gribkovie_chamfer,
)
from src.tool_updater.jobs.turn_mill_gribkovie_flat import (
    turn_mill_gribkovie_flat,
)
from src.tool_updater.jobs.turn_mill_gribkovie_rounding import (
    turn_mill_gribkovie_rounding,
)


def turn_mill_gribkovie() -> list[GenerationJob]:
    """Build jobs for the turn_mill_gribkovie group."""
    jobs: list[GenerationJob] = []
    jobs.extend(turn_mill_gribkovie_flat())
    jobs.extend(turn_mill_gribkovie_chamfer())
    jobs.extend(turn_mill_gribkovie_rounding())
    return jobs
