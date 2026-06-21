"""Layer-2 settings resolver mirrored from supabase_store_bridge.js."""

RM_SETTINGS_DEFAULTS = {
    "settings_version": 1,
    "house_system": "placidus",
    "zodiac_mode": "tropical",
    "orb_defaults": {
        "conjunction": 8,
        "square": 8,
        "opposition": 8,
        "trine": 8,
        "sextile": 6,
    },
    "visible_minor_aspects": False,
    "out_of_sign_aspects": False,
    "visible_planets": [
        "sun",
        "moon",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "uranus",
        "neptune",
        "pluto",
    ],
    "visible_bodies": ["chiron"],
    "visible_major_aspects": [
        "conjunction",
        "opposition",
        "square",
        "trine",
        "sextile",
    ],
    "visible_minor_aspects_list": [],
    "major_aspect_orbs": {
        "conjunction": 8,
        "square": 8,
        "opposition": 8,
        "trine": 8,
        "sextile": 6,
    },
    "minor_aspect_orbs": {
        "quincunx": 3,
        "semisextile": 2,
        "semisquare": 2,
        "sesquiquadrate": 2,
        "quintile": 2,
        "biquintile": 2,
    },
    "house_proximity_orb_degrees": 2,
    "subsequent_house_policy": "display_only",
    "aspect_to_angle_orbs": {
        "conjunction": 8,
        "opposition": 8,
        "square": 8,
        "trine": 8,
        "sextile": 6,
    },
    "helper_layers": {},
    "ontology_pack_id": None,
    # SETTINGS-WIRE-1A: which relocated angles to show in A2A tables and comparisons.
    # ASC/MC default ON; DSC/IC default OFF — conventional relocation focus.
    "display_aspects_to_angles": {
        "asc": True,
        "mc":  True,
        "dsc": False,
        "ic":  False,
    },
}


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
        "orb_defaults": effective_major_orbs,
        "visible_minor_aspects": pick("visible_minor_aspects"),
        "out_of_sign_aspects": pick("out_of_sign_aspects"),
        "visible_planets": pick("visible_planets"),
        "visible_bodies": pick("visible_bodies"),
        "visible_major_aspects": pick("visible_major_aspects"),
        "visible_minor_aspects_list": pick("visible_minor_aspects_list"),
        "major_aspect_orbs": effective_major_orbs,
        "minor_aspect_orbs": pick("minor_aspect_orbs"),
        "house_proximity_orb_degrees": house_prox,
        "subsequent_house_policy": pick("subsequent_house_policy"),
        "aspect_to_angle_orbs": pick("aspect_to_angle_orbs"),
        "helper_layers": pick("helper_layers"),
        "ontology_pack_id": pick("ontology_pack_id"),
        # SETTINGS-WIRE-1A
        "display_aspects_to_angles": (
            stored.get("display_aspects_to_angles")
            or onto.get("display_aspects_to_angles")
            or RM_SETTINGS_DEFAULTS["display_aspects_to_angles"]
        ),
    }
