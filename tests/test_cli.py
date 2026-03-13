"""Tests for medium_modulation CLI commands."""

import re

from typer.testing import CliRunner

from medium_modulation.cli import app

runner = CliRunner()


class TestModulateCommand:
    def test_default_run(self):
        result = runner.invoke(app, ["modulate"])
        assert result.exit_code == 0
        assert "Modulation Results" in result.output

    def test_custom_depth_freq(self):
        result = runner.invoke(app, ["modulate", "--depth", "0.7", "--freq", "2.3"])
        assert result.exit_code == 0
        assert "Mean S_mod" in result.output

    def test_depth_zero(self):
        result = runner.invoke(app, ["modulate", "--depth", "0.0"])
        assert result.exit_code == 0

    def test_steps_param(self):
        result = runner.invoke(app, ["modulate", "--steps", "10"])
        assert result.exit_code == 0

    def test_custom_s_a_s_v(self):
        result = runner.invoke(app, ["modulate", "--s-a", "2.0", "--s-v", "3.0"])
        assert result.exit_code == 0


class TestSpectrumCommand:
    def test_default_run(self):
        result = runner.invoke(app, ["spectrum"])
        assert result.exit_code == 0
        assert "Resonance Spectrum" in result.output

    def test_custom_range(self):
        result = runner.invoke(
            app, ["spectrum", "--f-min", "0.5", "--f-max", "5.0", "--n", "20"]
        )
        assert result.exit_code == 0
        assert "Peak amplitude" in result.output

    def test_depth_zero_peak_one(self):
        result = runner.invoke(app, ["spectrum", "--depth", "0.0"])
        assert result.exit_code == 0
        assert "1.000000" in result.output


class TestCoupleCommand:
    def test_default_run(self):
        result = runner.invoke(app, ["couple"])
        assert result.exit_code == 0
        assert "Coupling factor" in result.output

    def test_custom_a_v(self):
        result = runner.invoke(app, ["couple", "--a", "2.0", "--v", "3.0"])
        assert result.exit_code == 0

    def test_output_contains_numeric(self):
        result = runner.invoke(
            app, ["couple", "--a", "1.0", "--v", "1.0", "--depth", "0.0"]
        )
        assert result.exit_code == 0
        assert re.search(r"\d+\.\d+", result.output)
