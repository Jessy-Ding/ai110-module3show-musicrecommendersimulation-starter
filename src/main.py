"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Richer taste profile with weighted categories and numeric tolerances.
    user_prefs = {
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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
