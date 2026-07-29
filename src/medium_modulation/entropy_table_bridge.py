"""Bridge between medium-modulation and entropy-table domain registry."""

from __future__ import annotations

from pathlib import Path

import yaml  # type: ignore


class MediumModulationBridge:
    """Stores modulation relations and exports them to domains.yaml format."""

    DOMAIN = "medium-modulation"

    def __init__(self) -> None:
        self._relations: dict[str, float] = {}

    def add_modulation(self, key: str, value: float) -> None:
        """Register a named modulation value."""
        self._relations[key] = float(value)

    def export(self, filepath: Path | str = "domains.yaml") -> Path:
        """Serialise relations to a YAML file and return the path."""
        filepath = Path(filepath)
        data: dict = {}

        if filepath.exists():
            with filepath.open() as fh:
                data = yaml.safe_load(fh) or {}

        data.setdefault("domains", {}).setdefault(self.DOMAIN, {}).update(
            self._relations
        )

        with filepath.open("w") as fh:
            yaml.safe_dump(data, fh, default_flow_style=False, allow_unicode=True)

        return filepath

    def relations(self) -> dict[str, float]:
        """Return a copy of the currently registered relations."""
        return dict(self._relations)
