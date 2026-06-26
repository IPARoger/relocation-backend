"""Layer-2 settings resolver — defaults from settings/astrology_settings_defaults.json."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

_DEFAULTS_PATH = Path(__file__).resolve().parent.parent / "settings" / "astrology_settings_defaults.json"
_APPEARANCE_DEFAULTS_PATH = Path(__file__).resolve().parent.parent / "settings" / "appearance_settings_defaults.json"


def load_astrology_settings_defaults() -> dict:
    with open(_DEFAULTS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_appearance_settings_defaults() -> dict:
    with open(_APPEARANCE_DEFAULTS_PATH, encoding="utf-8") as f:
        return json.load(f)


RM_SETTINGS_DEFAULTS: dict = load_astrology_settings_defaults()
RM_APPEARANCE_DEFAULTS: dict = load_appearance_settings_defaults()


def aspect_to_angle_orb_limit(effective_settings: dict, aspect: str) -> float:
    """Orb limit for A2A compute — settings registry only, no hidden literals."""
    a2a_orbs = effective_settings.get("aspect_to_angle_orbs")
    if not isinstance(a2a_orbs, dict):
        a2a_orbs = RM_SETTINGS_DEFAULTS["aspect_to_angle_orbs"]
    if aspect in a2a_orbs:
        return float(a2a_orbs[aspect])
    major_orbs = effective_settings.get("major_aspect_orbs") or RM_SETTINGS_DEFAULTS["major_aspect_orbs"]
    if aspect in major_orbs:
        return float(major_orbs[aspect])
    default_a2a = RM_SETTINGS_DEFAULTS["aspect_to_angle_orbs"]
    if aspect in default_a2a:
        return float(default_a2a[aspect])
    default_major = RM_SETTINGS_DEFAULTS["major_aspect_orbs"]
    return float(default_major.get(aspect, default_major.get("conjunction", 8)))


def chart_display_orb_limit(effective_settings: dict, aspect: str, *, is_minor: bool = False) -> float:
    """Orb limit for P2P chart-display aspects — major/minor_aspect_orbs only."""
    key = "minor_aspect_orbs" if is_minor else "major_aspect_orbs"
    orbs = effective_settings.get(key)
    if not isinstance(orbs, dict):
        orbs = RM_SETTINGS_DEFAULTS[key]
    if aspect in orbs:
        return float(orbs[aspect])
    defaults = RM_SETTINGS_DEFAULTS[key]
    if aspect in defaults:
        return float(defaults[aspect])
    fallback = defaults.get("conjunction") if not is_minor else defaults.get("quincunx", 2)
    return float(fallback)


def get_effective_settings(stored_user_settings=None, ontology_defaults=None):
    stored = stored_user_settings if isinstance(stored_user_settings, dict) else {}
    onto = ontology_defaults if isinstance(ontology_defaults, dict) else {}

    def pick(key):
        if stored.get(key) not in (None, ""):
            return stored[key]
        if onto.get(key) not in (None, ""):
            return onto[key]
        return RM_SETTINGS_DEFAULTS[key]

    effective_major_orbs = (
        stored.get("major_aspect_orbs")
        or stored.get("orb_defaults")
        or onto.get("major_aspect_orbs")
        or onto.get("orb_defaults")
        or RM_SETTINGS_DEFAULTS["major_aspect_orbs"]
    )

    house_prox = stored.get("house_proximity_orb_degrees")
    if house_prox is None:
        house_prox = onto.get("house_proximity_orb_degrees")
    if house_prox is None:
        house_prox = RM_SETTINGS_DEFAULTS["house_proximity_orb_degrees"]

    return {
        "settings_version": pick("settings_version"),
        "house_system": pick("house_system"),
        "zodiac_mode": pick("zodiac_mode"),
        "orb_defaults": deepcopy(effective_major_orbs),
        "visible_minor_aspects": pick("visible_minor_aspects"),
        "out_of_sign_aspects": pick("out_of_sign_aspects"),
        "visible_planets": pick("visible_planets"),
        "visible_bodies": pick("visible_bodies"),
        "visible_major_aspects": pick("visible_major_aspects"),
        "visible_minor_aspects_list": pick("visible_minor_aspects_list"),
        "major_aspect_orbs": deepcopy(effective_major_orbs),
        "minor_aspect_orbs": pick("minor_aspect_orbs"),
        "house_proximity_orb_degrees": house_prox,
        "subsequent_house_policy": pick("subsequent_house_policy"),
        "aspect_to_angle_orbs": pick("aspect_to_angle_orbs"),
        "helper_layers": pick("helper_layers"),
        "ontology_pack_id": pick("ontology_pack_id"),
        "display_aspects_to_angles": (
            stored.get("display_aspects_to_angles")
            or onto.get("display_aspects_to_angles")
            or deepcopy(RM_SETTINGS_DEFAULTS["display_aspects_to_angles"])
        ),
        "exact_aspect_threshold_deg": pick("exact_aspect_threshold_deg"),
        "dignity_preset": pick("dignity_preset") or RM_SETTINGS_DEFAULTS.get("dignity_preset", "hybrid"),
        "dignity_custom_rules": pick("dignity_custom_rules") or [],
        "dignity_color_mode": pick("dignity_color_mode") or RM_SETTINGS_DEFAULTS.get("dignity_color_mode", "paired"),
        "dignity_colors": pick("dignity_colors") or deepcopy(RM_SETTINGS_DEFAULTS.get("dignity_colors", {})),
        "overlay_palette": pick("overlay_palette") or RM_APPEARANCE_DEFAULTS.get("overlay_palette", "optimistic-primary"),
        "aspect_palette": pick("aspect_palette") or RM_APPEARANCE_DEFAULTS.get("aspect_palette", "optimistic-primary"),
        "dignity_palette": pick("dignity_palette") or RM_APPEARANCE_DEFAULTS.get("dignity_palette", "optimistic-soft"),
        "chart_palette": pick("chart_palette") or RM_APPEARANCE_DEFAULTS.get("chart_palette", "optimistic-primary"),
        "inner_glow_palette": pick("inner_glow_palette") or RM_APPEARANCE_DEFAULTS.get("inner_glow_palette", "micro-green"),
        "glyph_selections": (
            stored.get("glyph_selections")
            or onto.get("glyph_selections")
            or deepcopy(RM_SETTINGS_DEFAULTS.get("glyph_selections", {}))
        ),
    }

def exact_aspect_threshold_deg(effective_settings: dict) -> float:
    raw = effective_settings.get("exact_aspect_threshold_deg")
    if raw is None:
        raw = RM_SETTINGS_DEFAULTS.get("exact_aspect_threshold_deg", 0.5)
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.5

