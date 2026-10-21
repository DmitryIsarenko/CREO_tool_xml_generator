"""Catalog jobs for turn_mill_gribkovie_flat."""

from src.tool_updater.jobs.model import GenerationJob


def turn_mill_gribkovie_flat() -> list[GenerationJob]:
    """Build jobs for the turn_mill_gribkovie_flat group."""
    jobs: list[GenerationJob] = []
    return jobs
