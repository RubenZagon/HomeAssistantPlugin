"""Tests for the fan mode helpers.

fan_modes.py has no Home Assistant imports, so it is loaded straight from its
file: importing the integration package would pull in Home Assistant.
"""
import importlib.util
from pathlib import Path

import pytest

_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "hisense_ac_plugin"
    / "fan_modes.py"
)
_SPEC = importlib.util.spec_from_file_location("hisense_fan_modes", _PATH)
fan_modes = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fan_modes)


@pytest.mark.parametrize(
    ("desc", "expected"),
    [
        # Short forms
        ("自动", "auto"),
        ("低", "low"),
        ("中", "medium"),
        ("高", "high"),
        # Long forms reported by some devices (the portable air conditioner)
        ("低风", "low"),
        ("中风", "medium"),
        ("高风", "high"),
        # English descriptions
        ("auto", "auto"),
        ("low", "low"),
        ("medium", "medium"),
        ("med", "medium"),
        ("high", "high"),
        # Case and surrounding spaces are ignored
        ("AUTO", "auto"),
        (" 低风 ", "low"),
        # Ultra speeds keep the existing (non standard) names
        ("超低", fan_modes.SFAN_ULTRA_LOW),
        ("超低风", fan_modes.SFAN_ULTRA_LOW),
        ("ultra low", fan_modes.SFAN_ULTRA_LOW),
        ("超高", fan_modes.SFAN_ULTRA_HIGH),
        ("超高风", fan_modes.SFAN_ULTRA_HIGH),
        ("ultra high", fan_modes.SFAN_ULTRA_HIGH),
    ],
)
def test_fan_desc_to_mode(desc, expected):
    """Known descriptions map to the expected fan mode."""
    assert fan_modes.fan_desc_to_mode(desc) == expected


@pytest.mark.parametrize("desc", ["", "turbo", "中低", "中高", "风"])
def test_fan_desc_to_mode_unknown(desc):
    """Unknown descriptions return None so the caller keeps the raw text."""
    assert fan_modes.fan_desc_to_mode(desc) is None


def test_standard_mode_names():
    """The standard names are the ones Home Assistant translates."""
    assert fan_modes.FAN_AUTO == "auto"
    assert fan_modes.FAN_LOW == "low"
    assert fan_modes.FAN_MEDIUM == "medium"
    assert fan_modes.FAN_HIGH == "high"
