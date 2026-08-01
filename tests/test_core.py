"""Tests for medium_modulation.core."""

import numpy as np
import pytest

from medium_modulation.core import (
    coupling_factor,
    modulated_entropy,
    resonance_spectrum,
)

_PHI = 0.618033988749895


class TestModulatedEntropy:
    def test_zero_depth_returns_duality_factor(self):
        # With depth=0 the modulation term vanishes → α·S_A + (1-α)·S_V
        result = modulated_entropy(1.0, 1.618, depth=0.0, freq=1.0, t=0.0)
        expected = _PHI * 1.0 + (1.0 - _PHI) * 1.618
        assert result == pytest.approx(expected, rel=1e-6)

    def test_known_value(self):
        # depth=0 at t=0: S_mod = φ·1.0 + (1-φ)·1.618 ≈ 1.236
        result = modulated_entropy(1.0, 1.618, depth=0.0)
        assert result == pytest.approx(1.236, abs=0.01)

    def test_depth_increases_modulation(self):
        s_no_mod = modulated_entropy(1.0, 1.0, depth=0.0, freq=1.0, t=1.0)
        s_with_mod = modulated_entropy(1.0, 1.0, depth=0.9, freq=1.0, t=1.0)
        # With depth>0 and sin(1)>0 the action term should be boosted
        assert s_with_mod != s_no_mod

    def test_symmetry_at_pi(self):
        # sin(π) ≈ 0 → modulation ≈ 1 → same as depth=0
        result = modulated_entropy(1.0, 1.618, depth=0.5, freq=1.0, t=np.pi)
        expected = modulated_entropy(1.0, 1.618, depth=0.0)
        assert result == pytest.approx(expected, rel=1e-5)

    def test_returns_float(self):
        result = modulated_entropy(2.0, 3.0)
        assert isinstance(result, float)

    def test_different_s_a_s_v(self):
        r1 = modulated_entropy(1.0, 2.0, depth=0.0)
        r2 = modulated_entropy(2.0, 1.0, depth=0.0)
        assert r1 != r2


class TestResonanceSpectrum:
    def test_shape_preserved(self):
        freqs = np.linspace(0.1, 10, 50)
        spec = resonance_spectrum(freqs)
        assert spec.shape == (50,)

    def test_zero_depth_returns_ones(self):
        freqs = np.linspace(0, 5, 20)
        spec = resonance_spectrum(freqs, depth=0.0)
        np.testing.assert_allclose(spec, np.ones(20))

    def test_amplitude_bounds(self):
        freqs = np.linspace(0.1, 10, 100)
        spec = resonance_spectrum(freqs, depth=0.5)
        assert spec.min() >= 0.5 - 1e-9
        assert spec.max() <= 1.5 + 1e-9

    def test_peak_at_depth_one(self):
        freqs = np.linspace(0.1, 10, 200)
        spec = resonance_spectrum(freqs, depth=1.0)
        assert spec.max() == pytest.approx(2.0, rel=1e-3)

    def test_accepts_list_input(self):
        spec = resonance_spectrum([0.25, 0.5, 0.75], depth=0.5)
        assert len(spec) == 3

    def test_returns_ndarray(self):
        spec = resonance_spectrum(np.array([1.0, 2.0]))
        assert isinstance(spec, np.ndarray)


class TestCouplingFactor:
    def test_returns_float(self):
        result = coupling_factor(1.0, 1.618)
        assert isinstance(result, float)

    def test_zero_depth_equals_duality(self):
        result = coupling_factor(1.0, 1.618, modulation_depth=0.0)
        expected = modulated_entropy(1.0, 1.618, depth=0.0)
        assert result == pytest.approx(expected)

    def test_varies_with_depth(self):
        r1 = coupling_factor(1.0, 1.0, modulation_depth=0.0)
        r2 = coupling_factor(1.0, 1.0, modulation_depth=0.5)
        # Evaluated at the modulation peak, so depth must have a real,
        # monotonic effect (previously always t=0 -> sin(0)=0 -> no effect
        # regardless of depth; see medium-modulation-blindtest).
        assert r2 > r1

    def test_a_v_influence(self):
        r1 = coupling_factor(1.0, 1.0)
        r2 = coupling_factor(2.0, 1.0)
        assert r2 > r1
