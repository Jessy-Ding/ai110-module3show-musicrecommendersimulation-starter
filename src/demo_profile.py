"""Named demo user preferences for quick CLI experiments."""

HIGH_ENERGY_POP_PREFS = {
    "weighting_scheme": "balanced",
    "preferred_genres": {"pop": 1.0},
    "favorite_moods": {"happy": 1.0},
    "target_energy": 0.78,
    "energy_tolerance": 0.20,
    "target_tempo_bpm": 120,
    "tempo_tolerance_bpm": 16,
    "target_valence": 0.80,
    "valence_tolerance": 0.18,
    "target_danceability": 0.82,
    "danceability_tolerance": 0.15,
    "target_acousticness": 0.18,
    "acousticness_tolerance": 0.15,
    "excluded_genres": ["lofi"],
    "novelty_preference": 0.25,
    "diversity_boost": 0.20,
}

CHILL_LOFI_PREFS = {
    "weighting_scheme": "balanced",
    "preferred_genres": {"lofi": 1.0, "ambient": 0.5},
    "favorite_moods": {"chill": 1.0, "relaxed": 0.7},
    "target_energy": 0.38,
    "energy_tolerance": 0.18,
    "target_tempo_bpm": 78,
    "tempo_tolerance_bpm": 14,
    "target_valence": 0.58,
    "valence_tolerance": 0.20,
    "target_danceability": 0.60,
    "danceability_tolerance": 0.14,
    "target_acousticness": 0.75,
    "acousticness_tolerance": 0.18,
    "excluded_genres": ["metal"],
    "novelty_preference": 0.15,
    "diversity_boost": 0.10,
}

DEEP_INTENSE_ROCK_PREFS = {
    "weighting_scheme": "conservative",
    "preferred_genres": {"rock": 1.0, "metal": 0.7},
    "favorite_moods": {"intense": 1.0, "confident": 0.5},
    "target_energy": 0.90,
    "energy_tolerance": 0.16,
    "target_tempo_bpm": 150,
    "tempo_tolerance_bpm": 20,
    "target_valence": 0.45,
    "valence_tolerance": 0.18,
    "target_danceability": 0.62,
    "danceability_tolerance": 0.15,
    "target_acousticness": 0.12,
    "acousticness_tolerance": 0.12,
    "excluded_genres": ["lofi", "classical"],
    "novelty_preference": 0.10,
    "diversity_boost": 0.08,
}

# Adversarial profiles for system-evaluation stress tests.
CONFLICT_ENERGY_SAD_PREFS = {
    "weighting_scheme": "balanced",
    "preferred_genres": {"pop": 1.0},
    "favorite_moods": {"sad": 1.0},
    "target_energy": 0.90,
    "energy_tolerance": 0.08,
    "target_tempo_bpm": 95,
    "tempo_tolerance_bpm": 10,
    "target_valence": 0.20,
    "valence_tolerance": 0.10,
    "target_danceability": 0.85,
    "danceability_tolerance": 0.10,
    "target_acousticness": 0.10,
    "acousticness_tolerance": 0.08,
    "novelty_preference": 0.00,
    "diversity_boost": 0.00,
}

SELF_CONTRADICT_EXCLUDE_ONLY_GENRE_PREFS = {
    "weighting_scheme": "conservative",
    "preferred_genres": {"metal": 1.0},
    "favorite_moods": {"intense": 1.0},
    "excluded_genres": ["metal"],
    "target_energy": 0.95,
    "energy_tolerance": 0.08,
    "target_tempo_bpm": 160,
    "tempo_tolerance_bpm": 12,
    "target_valence": 0.35,
    "valence_tolerance": 0.10,
    "target_danceability": 0.55,
    "danceability_tolerance": 0.10,
    "target_acousticness": 0.05,
    "acousticness_tolerance": 0.07,
    "novelty_preference": 0.00,
    "diversity_boost": 0.00,
}

ZERO_TOLERANCE_TRAP_PREFS = {
    "weighting_scheme": "balanced",
    "preferred_genres": {"lofi": 1.0},
    "favorite_moods": {"chill": 1.0},
    "target_energy": 0.34,
    "energy_tolerance": 0.00,
    "target_tempo_bpm": 77,
    "tempo_tolerance_bpm": 0,
    "target_valence": 0.58,
    "valence_tolerance": 0,
    "target_danceability": 0.54,
    "danceability_tolerance": 0,
    "target_acousticness": 0.82,
    "acousticness_tolerance": 0,
    "novelty_preference": 0.00,
    "diversity_boost": 0.00,
}

NOVELTY_MAX_NO_PREFS_PREFS = {
    "weighting_scheme": "exploratory",
    "preferred_genres": {},
    "favorite_moods": {},
    "novelty_preference": 1.00,
    "target_energy": 0.50,
    "energy_tolerance": 0.40,
    "target_tempo_bpm": 110,
    "tempo_tolerance_bpm": 40,
    "target_valence": 0.50,
    "valence_tolerance": 0.40,
    "target_danceability": 0.60,
    "danceability_tolerance": 0.40,
    "target_acousticness": 0.40,
    "acousticness_tolerance": 0.40,
    "diversity_boost": 0.00,
}

PROFILE_LIBRARY = {
    "high_energy_pop": HIGH_ENERGY_POP_PREFS,
    "chill_lofi": CHILL_LOFI_PREFS,
    "deep_intense_rock": DEEP_INTENSE_ROCK_PREFS,
    "conflict_energy_sad": CONFLICT_ENERGY_SAD_PREFS,
    "self_contradict_exclude_only_genre": SELF_CONTRADICT_EXCLUDE_ONLY_GENRE_PREFS,
    "zero_tolerance_trap": ZERO_TOLERANCE_TRAP_PREFS,
    "novelty_max_no_prefs": NOVELTY_MAX_NO_PREFS_PREFS,
}

# Default profile used by src/main.py
DEMO_USER_PREFS = HIGH_ENERGY_POP_PREFS
