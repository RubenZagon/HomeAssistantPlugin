"""Fan mode helpers for the Hisense AC Plugin integration.

This module has no Home Assistant imports so it can be unit tested on its own.
"""
from __future__ import annotations

# Fan Modes
FAN_AUTO = "auto"
FAN_ULTRA_LOW = "ultra_low"
SFAN_ULTRA_LOW = "中低"
FAN_LOW = "low"
FAN_MEDIUM = "medium"
FAN_HIGH = "high"
FAN_ULTRA_HIGH = "ultra_high"
SFAN_ULTRA_HIGH = "中高"


def fan_desc_to_mode(desc: str) -> str | None:
    """Map a fan speed description from the cloud to a standard HA fan mode.

    The cloud reports either the short form ("低") or the long form ("低风"),
    depending on the device, so the trailing "风" (wind) is ignored. Returns
    None when the description is unknown.
    """
    d = desc.strip().lower()
    if d.endswith("风"):
        d = d[:-1]
    if d in ("自动", "auto"):
        return FAN_AUTO
    if d in ("超低", "ultra low"):
        return SFAN_ULTRA_LOW
    if d in ("低", "low"):
        return FAN_LOW
    if d in ("中", "medium", "med"):
        return FAN_MEDIUM
    if d in ("高", "high"):
        return FAN_HIGH
    if d in ("超高", "ultra high"):
        return SFAN_ULTRA_HIGH
    return None
