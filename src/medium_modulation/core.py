"""Fractal modulation operators and resonance coupling for medium-modulation."""

import numpy as np
import sympy as sp

# Golden ratio – the natural coupling constant
_PHI = 0.618033988749895

t_sym, omega, phi_sym = sp.symbols("t omega phi", real=True, positive=True)
depth_sym = sp.symbols("depth", positive=True)

# Symbolic modulation operator M(t) = 1 + depth · sin(ωt + φ)
M = 1 + depth_sym * sp.sin(omega * t_sym + phi_sym)


def _duality_factor(S_A: float, S_V: float, alpha: float = _PHI) -> float:
    """Weighted duality: α·S_A + (1-α)·S_V."""
    return alpha * S_A + (1.0 - alpha) * S_V


def modulated_entropy(
    S_A: float,
    S_V: float,
    depth: float = 0.5,
    freq: float = 1.0,
    t: float = 0.0,
) -> float:
    """Fractal medium modulation: S_mod = α·(S_A·M) + (1-α)·S_V.

    Parameters
    ----------
    S_A:   action-governed entropy
    S_V:   volume-governed entropy
    depth: modulation depth ∈ [0, 1]
    freq:  modulation frequency (rad/s)
    t:     time point

    Returns
    -------
    Modulated composite entropy value.
    """
    modulation = 1.0 + depth * np.sin(freq * t)
    return _duality_factor(S_A * modulation, S_V, alpha=_PHI)


def resonance_spectrum(freqs: np.ndarray, depth: float = 0.5) -> np.ndarray:
    """Resonance spectrum evaluated over a frequency array.

    Parameters
    ----------
    freqs: 1-D array of frequencies
    depth: modulation depth ∈ [0, 1]

    Returns
    -------
    Array of resonance amplitudes.
    """
    freqs = np.asarray(freqs, dtype=float)
    return 1.0 + depth * np.sin(2.0 * np.pi * freqs)


def coupling_factor(A: float, V: float, modulation_depth: float = 0.5) -> float:
    """Dynamic coupling strength between action and volume at t=0.

    Parameters
    ----------
    A:                action amplitude
    V:                volume amplitude
    modulation_depth: depth of the modulation operator

    Returns
    -------
    Scalar coupling strength.
    """
    return modulated_entropy(A, V, depth=modulation_depth, freq=1.0, t=0.0)
