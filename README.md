# medium-modulation

**The resonant medium between action and expanse.**

[![CI](https://github.com/GenesisAeon/medium-modulation/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/medium-modulation/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

medium-modulation serves as the dynamic coupling layer that modulates the fundamental duality of the GenesisAeon framework: action-governed entropy production (S ∝ A) versus volume-governed informational expansion (S ∝ V).

Through fractal modulation operators, resonance spectra, and tunable interference fields, it turns raw tension into coherent emergence.

---

## Install

```bash
pip install medium-modulation
```

## Usage

```bash
mm modulate --depth 0.7 --freq 2.3
mm spectrum
```

## API

```python
from medium_modulation.core import modulated_entropy, resonance_spectrum, coupling_factor
import numpy as np

# Fractal medium modulation
S_mod = modulated_entropy(S_A=1.0, S_V=1.618, depth=0.5, freq=1.0, t=0.0)

# Resonance spectrum over frequency range
freqs = np.linspace(0.1, 10, 50)
spec = resonance_spectrum(freqs, depth=0.5)

# Dynamic coupling strength
kappa = coupling_factor(A=1.0, V=1.618, modulation_depth=0.5)
```

## Architecture

```
medium-modulation/
├── src/medium_modulation/
│   ├── core.py                  # Modulation operator + fractal coupling
│   ├── cli.py                   # CLI mm
│   └── entropy_table_bridge.py  # entropy-table integration
├── tests/
│   ├── test_core.py
│   └── test_cli.py
└── domains.yaml                 # Domain configuration
```

## Integrations

| Package | Role |
|---------|------|
| `entropy-governance` | Duality factor α·S_A + (1-α)·S_V |
| `entropy-table` | Domain relation registry |
| `implosive-genesis` | Fractal emergence substrate |

**DOI** (after Zenodo release): 10.5281/zenodo.XXXXXXX
**PyPI**: https://pypi.org/project/medium-modulation/

---

Built with [SymPy](https://www.sympy.org/) · [NumPy](https://numpy.org/) · [Typer](https://typer.tiangolo.com/) · [Rich](https://rich.readthedocs.io/)
