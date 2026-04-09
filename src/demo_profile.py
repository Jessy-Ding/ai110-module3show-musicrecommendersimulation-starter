"""Demo user preferences for the music recommender simulation.

Keeping this separate from main.py makes the entry point easier to read and
lets you swap in different profiles without changing the program flow.
"""

DEMO_USER_PREFS = {
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
