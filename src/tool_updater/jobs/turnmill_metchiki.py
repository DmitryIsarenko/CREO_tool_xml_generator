"""Catalog jobs for turnmill_metchiki."""

from src.tool_updater.jobs.model import GenerationJob
from src.tool_updater.jobs.turnmill_metchiki_blind import (
    turnmill_metchiki_blind,
)
from src.tool_updater.jobs.turnmill_metchiki_through import (
    turnmill_metchiki_through,
)


def turnmill_metchiki() -> list[GenerationJob]:
    """Build jobs for the turnmill_metchiki group."""
    jobs: list[GenerationJob] = []
    jobs.extend(turnmill_metchiki_blind())
    jobs.extend(turnmill_metchiki_through())
    return jobs
