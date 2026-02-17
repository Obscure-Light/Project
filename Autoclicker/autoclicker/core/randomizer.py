"""Utilities for humanized interval generation."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(slots=True)
class RandomizationSettings:
    """Controls how interval jitter is generated."""

    enabled: bool = False
    stddev_percent: float = 5.0
    min_percent: float = -10.0
    max_percent: float = 10.0


def humanized_interval(base_seconds: float, settings: RandomizationSettings) -> float:
    """
    Return a humanized interval.

    Gaussian jitter is centered around the base interval and then clamped
    so the output always stays inside a deterministic safe range.
    """
    if not settings.enabled:
        return base_seconds

    # Sample a percentage delta from a normal distribution.
    sampled_delta = random.gauss(0.0, settings.stddev_percent)
    clamped_delta = max(settings.min_percent, min(settings.max_percent, sampled_delta))
    candidate = base_seconds * (1.0 + clamped_delta / 100.0)
    return max(0.05, candidate)
