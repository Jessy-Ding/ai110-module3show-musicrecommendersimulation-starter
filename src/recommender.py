import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


WEIGHT_SCHEMES: Dict[str, Dict[str, float]] = {
    # Genre-led: strongest anchor on genre identity.
    "conservative": {
        "genre_match": 0.34,
        "mood_match": 0.20,
        "energy_proximity": 0.16,
        "tempo_proximity": 0.11,
        "valence_proximity": 0.07,
        "danceability_proximity": 0.07,
        "acousticness_proximity": 0.05,
    },
    # Classroom default: genre and mood are close, with meaningful numeric signals.
    "balanced": {
        "genre_match": 0.24,
        "mood_match": 0.22,
        "energy_proximity": 0.16,
        "tempo_proximity": 0.13,
        "valence_proximity": 0.09,
        "danceability_proximity": 0.10,
        "acousticness_proximity": 0.06,
    },
    # Discovery-oriented: stronger mood and audio similarity influence.
    "exploratory": {
        "genre_match": 0.14,
        "mood_match": 0.26,
        "energy_proximity": 0.19,
        "tempo_proximity": 0.14,
        "valence_proximity": 0.10,
        "danceability_proximity": 0.11,
        "acousticness_proximity": 0.06,
    },
}

@dataclass
class Song:
    """Represents one song and its features."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """Represents a user's core taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """Implements OOP-style recommendation methods over Song objects."""
    def __init__(self, songs: List[Song]):
        """Stores the song catalog used for recommendation."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects ranked for a user profile."""
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            scored.append((song, _score_song_for_user(song, user)))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Builds a short natural-language explanation for one recommendation."""
        reasons: List[str] = []

        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("genre matches your favorite")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("mood matches your preference")

        energy_gap = abs(song.energy - user.target_energy)
        if energy_gap <= 0.15:
            reasons.append("energy is close to your target")

        if user.likes_acoustic and song.acousticness >= 0.5:
            reasons.append("it has an acoustic character")
        if not user.likes_acoustic and song.acousticness < 0.5:
            reasons.append("it avoids heavy acoustic texture")

        if not reasons:
            return "This track is a moderate match across several features."
        return "; ".join(reasons) + "."


def _closeness(value: float, target: float, tolerance: float) -> float:
    """Returns normalized similarity based on target distance and tolerance."""
    if tolerance <= 0:
        return 1.0 if value == target else 0.0
    distance = abs(value - target)
    return max(0.0, 1.0 - (distance / tolerance))


def _weighted_lookup(name: str, weights: Dict[str, float]) -> float:
    """Looks up a lowercase key in a weights mapping and returns a float."""
    return float(weights.get(name.lower(), 0.0))


def _get_weight_scheme(user_prefs: Dict) -> Dict[str, float]:
    """Resolves the active weighting scheme from user preferences."""
    scheme_name = str(user_prefs.get("weighting_scheme", "balanced")).lower()
    return WEIGHT_SCHEMES.get(scheme_name, WEIGHT_SCHEMES["balanced"])


def _score_song_for_user(song: Song, user: UserProfile) -> float:
    """Scores a Song object for the OOP recommender path."""
    scheme = WEIGHT_SCHEMES["balanced"]
    score = 0.0

    if song.genre.lower() == user.favorite_genre.lower():
        score += scheme["genre_match"]
    if song.mood.lower() == user.favorite_mood.lower():
        score += scheme["mood_match"]

    score += scheme["energy_proximity"] * _closeness(song.energy, user.target_energy, 0.25)

    acoustic_pref = song.acousticness if user.likes_acoustic else (1.0 - song.acousticness)
    score += scheme["acousticness_proximity"] * acoustic_pref

    return score

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from CSV and returns typed song dictionaries."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def _score_song_dict(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song dict and returns both score and explanation reasons."""
    scheme = _get_weight_scheme(user_prefs)
    score = 0.0
    reasons: List[str] = []

    # Accept both new schema (preferred_genres) and legacy key (favorite_genre).
    preferred_genres: Dict[str, float] = {
        k.lower(): float(v) for k, v in user_prefs.get("preferred_genres", {}).items()
    }
    if not preferred_genres and "favorite_genre" in user_prefs:
        preferred_genres = {str(user_prefs["favorite_genre"]).lower(): 1.0}

    favorite_moods: Dict[str, float] = {
        k.lower(): float(v) for k, v in user_prefs.get("favorite_moods", {}).items()
    }
    if not favorite_moods and "favorite_mood" in user_prefs:
        favorite_moods = {str(user_prefs["favorite_mood"]).lower(): 1.0}

    excluded_genres = {g.lower() for g in user_prefs.get("excluded_genres", [])}
    novelty_preference = float(user_prefs.get("novelty_preference", 0.0))

    genre = str(song.get("genre", "")).lower()
    mood = str(song.get("mood", "")).lower()

    genre_weight = _weighted_lookup(genre, preferred_genres)
    if genre_weight > 0:
        contribution = scheme["genre_match"] * min(1.0, genre_weight)
        score += contribution
        reasons.append(f"genre match (+{contribution:.2f})")

    mood_weight = _weighted_lookup(mood, favorite_moods)
    if mood_weight > 0:
        contribution = scheme["mood_match"] * min(1.0, mood_weight)
        score += contribution
        reasons.append(f"mood match (+{contribution:.2f})")

    if genre in excluded_genres:
        contribution = -0.20
        score += contribution
        reasons.append(f"excluded genre ({contribution:.2f})")

    numeric_specs = [
        ("energy", "target_energy", "energy_tolerance", "energy_proximity", 0.25),
        ("tempo_bpm", "target_tempo_bpm", "tempo_tolerance_bpm", "tempo_proximity", 25.0),
        ("valence", "target_valence", "valence_tolerance", "valence_proximity", 0.30),
        ("danceability", "target_danceability", "danceability_tolerance", "danceability_proximity", 0.25),
        ("acousticness", "target_acousticness", "acousticness_tolerance", "acousticness_proximity", 0.30),
    ]

    for feature, target_key, tolerance_key, weight_key, default_tolerance in numeric_specs:
        if target_key in user_prefs:
            value = float(song[feature])
            target = float(user_prefs[target_key])
            tolerance = float(user_prefs.get(tolerance_key, default_tolerance))
            closeness = _closeness(value, target, tolerance)
            contribution = scheme[weight_key] * closeness
            score += contribution
            reasons.append(f"{feature} proximity (+{contribution:.2f})")

    # Small exploration bump for off-profile songs when novelty is desired.
    if novelty_preference > 0 and genre_weight == 0 and mood_weight == 0:
        # Exploration term is stronger in exploratory mode.
        exploration_scale = 0.04 if scheme is WEIGHT_SCHEMES["conservative"] else 0.05
        if scheme is WEIGHT_SCHEMES["exploratory"]:
            exploration_scale = 0.08
        contribution = exploration_scale * min(1.0, novelty_preference)
        score += contribution
        reasons.append(f"novelty bonus (+{contribution:.2f})")

    return score, reasons


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song for a user and returns (score, reasons)."""
    return _score_song_dict(user_prefs, song)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Ranks all songs by score and returns top-k with explanation strings."""
    scored: List[Tuple[Dict, float, str]] = [
        (
            song,
            score,
            ", ".join(reasons) if reasons else "overall profile proximity",
        )
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # Diversity boost: gently favor unseen genres in top-k when requested.
    diversity_boost = float(user_prefs.get("diversity_boost", 0.0))
    if diversity_boost <= 0:
        return ranked[:k]

    selected: List[Tuple[Dict, float, str]] = []
    seen_genres = set()

    for song, score, explanation in ranked:
        genre = str(song.get("genre", "")).lower()
        adjusted = score
        if genre not in seen_genres:
            adjusted += 0.08 * min(1.0, diversity_boost)
        selected.append((song, adjusted, explanation))
        seen_genres.add(genre)
        if len(selected) >= k:
            break

    return sorted(selected, key=lambda item: item[1], reverse=True)
