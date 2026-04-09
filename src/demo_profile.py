"""Demo user preferences for the music recommender simulation.

Keeping this separate from main.py makes the entry point easier to read and
lets you swap in different profiles without changing the program flow.
"""

DEMO_USER_PREFS = {
    "weighting_scheme": "balanced",
    "preferred_genres": {"house": 1.0, "synthwave": 0.6, "pop": 0.3},
    "favorite_moods": {"euphoric": 1.0, "happy": 0.5},
    "target_energy": 0.86,
    "energy_tolerance": 0.18,
    "target_tempo_bpm": 124,
    "tempo_tolerance_bpm": 18,
    "target_valence": 0.78,
    "valence_tolerance": 0.20,
    "target_danceability": 0.88,
    "danceability_tolerance": 0.15,
    "target_acousticness": 0.12,
    "acousticness_tolerance": 0.18,
    "excluded_genres": ["lofi"],
    "novelty_preference": 0.25,
    "diversity_boost": 0.20,
}
