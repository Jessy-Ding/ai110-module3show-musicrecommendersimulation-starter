"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

try:
    from .demo_profile import DEMO_USER_PREFS, PROFILE_LIBRARY
    from .recommender import load_songs, recommend_songs
except ImportError:
    from demo_profile import DEMO_USER_PREFS, PROFILE_LIBRARY
    from recommender import load_songs, recommend_songs


def _print_top_recommendations(profile_name: str, recommendations) -> None:
    """Prints top recommendations for one profile as an ASCII summary table."""

    def _build_separator(widths) -> str:
        return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def _build_row(values, widths) -> str:
        cells = [f" {str(value):<{widths[idx]}} " for idx, value in enumerate(values)]
        return "|" + "|".join(cells) + "|"

    headers = ["#", "Title", "Artist", "Genre", "Mood", "Score", "Reasons"]
    rows = []
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = "; ".join(r.strip() for r in explanation.split(",") if r.strip())
        rows.append(
            [
                index,
                song["title"],
                song["artist"],
                song["genre"],
                song["mood"],
                f"{score:.2f}",
                reasons,
            ]
        )

    widths = [
        max(len(str(headers[idx])), max((len(str(row[idx])) for row in rows), default=0))
        for idx in range(len(headers))
    ]

    print(f"\n=== Profile: {profile_name} ===")
    separator = _build_separator(widths)
    print(separator)
    print(_build_row(headers, widths))
    print(separator)
    for row in rows:
        print(_build_row(row, widths))
    print(separator)


def _parse_args() -> argparse.Namespace:
    """Parses CLI options for dataset, top-k, and profile mode."""
    parser = argparse.ArgumentParser(description="Music Recommender CLI")
    parser.add_argument(
        "--data",
        default="data/songs.csv",
        help="CSV file to score (default: data/songs.csv)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of recommendations per profile (default: 5)",
    )
    parser.add_argument(
        "--all-profiles",
        action="store_true",
        help="Run recommendations for every profile in PROFILE_LIBRARY",
    )
    return parser.parse_args()


def main() -> None:
    """Runs the CLI demo: load songs, score them, and print top recommendations."""
    args = _parse_args()

    songs = load_songs(args.data)
    print(f"Loaded songs: {len(songs)}")

    if args.all_profiles:
        for profile_name, user_prefs in PROFILE_LIBRARY.items():
            recommendations = recommend_songs(user_prefs, songs, k=args.top_k)
            _print_top_recommendations(profile_name, recommendations)
        return

    recommendations = recommend_songs(DEMO_USER_PREFS, songs, k=args.top_k)

    _print_top_recommendations("demo_default", recommendations)


if __name__ == "__main__":
    main()
