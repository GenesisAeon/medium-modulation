"""Tests for medium_modulation.entropy_table_bridge."""

import pytest
import yaml

from medium_modulation.entropy_table_bridge import MediumModulationBridge


class TestMediumModulationBridge:
    def test_bridge_export(self, tmp_path):
        bridge = MediumModulationBridge()
        bridge.add_modulation("coupling_baseline", 0.618)
        bridge.add_modulation("resonance_peak", 1.618)

        path = bridge.export(tmp_path / "test_domains.yaml")
        assert path.exists()

        data = yaml.safe_load(path.read_text())
        domain = data["domains"]["medium-modulation"]
        assert domain["coupling_baseline"] == pytest.approx(0.618)
        assert domain["resonance_peak"] == pytest.approx(1.618)

    def test_relations_returns_copy(self):
        bridge = MediumModulationBridge()
        bridge.add_modulation("alpha", 0.5)
        rel = bridge.relations()
        assert rel == {"alpha": 0.5}
        rel["alpha"] = 99.0
        assert bridge.relations()["alpha"] == pytest.approx(0.5)

    def test_export_merges_existing(self, tmp_path):
        path = tmp_path / "domains.yaml"
        existing = {"domains": {"other-domain": {"x": 1.0}}}
        path.write_text(yaml.safe_dump(existing))

        bridge = MediumModulationBridge()
        bridge.add_modulation("val", 2.0)
        bridge.export(path)

        data = yaml.safe_load(path.read_text())
        assert data["domains"]["other-domain"]["x"] == pytest.approx(1.0)
        assert data["domains"]["medium-modulation"]["val"] == pytest.approx(2.0)

    def test_export_returns_path(self, tmp_path):
        bridge = MediumModulationBridge()
        result = bridge.export(tmp_path / "out.yaml")
        assert isinstance(result, type(tmp_path / "out.yaml"))

    def test_domain_constant(self):
        assert MediumModulationBridge.DOMAIN == "medium-modulation"

    def test_empty_bridge_export(self, tmp_path):
        bridge = MediumModulationBridge()
        path = bridge.export(tmp_path / "empty.yaml")
        data = yaml.safe_load(path.read_text())
        assert data["domains"]["medium-modulation"] == {}

    def test_overwrite_existing_key(self, tmp_path):
        bridge = MediumModulationBridge()
        bridge.add_modulation("key", 1.0)
        bridge.export(tmp_path / "d.yaml")

        bridge2 = MediumModulationBridge()
        bridge2.add_modulation("key", 2.0)
        bridge2.export(tmp_path / "d.yaml")

        data = yaml.safe_load((tmp_path / "d.yaml").read_text())
        assert data["domains"]["medium-modulation"]["key"] == pytest.approx(2.0)
