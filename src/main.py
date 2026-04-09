"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .demo_profile import DEMO_USER_PREFS
    from .recommender import load_songs, recommend_songs
except ImportError:
    from demo_profile import DEMO_USER_PREFS
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = DEMO_USER_PREFS

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = [r.strip() for r in explanation.split(",") if r.strip()]

        print(f"{index}. {song['title']} by {song['artist']}")
        print(f"   Score  : {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
