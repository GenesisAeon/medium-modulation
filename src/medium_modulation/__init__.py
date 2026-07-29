"""medium-modulation: Resonant medium between S∝A and S∝V."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

try:
    __version__ = _version("medium-modulation")
except PackageNotFoundError:
    # Not installed, e.g. running from source.
    __version__ = "0.0.0+unknown"

from .core import coupling_factor, modulated_entropy, resonance_spectrum

__all__ = ["coupling_factor", "modulated_entropy", "resonance_spectrum"]
