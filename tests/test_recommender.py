from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_adaptive_exclusion_penalty_can_outweigh_category_matches():
    songs = [
        {
            "id": 1,
            "title": "Excluded Metal",
            "artist": "A",
            "genre": "metal",
            "mood": "intense",
            "energy": 0.95,
            "tempo_bpm": 160,
            "valence": 0.40,
            "danceability": 0.55,
            "acousticness": 0.05,
        },
        {
            "id": 2,
            "title": "Allowed Rock",
            "artist": "B",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.95,
            "tempo_bpm": 160,
            "valence": 0.40,
            "danceability": 0.55,
            "acousticness": 0.05,
        },
    ]
    user_prefs = {
        "weighting_scheme": "conservative",
        "preferred_genres": {"metal": 1.0},
        "favorite_moods": {"intense": 1.0},
        "excluded_genres": ["metal"],
    }

    ranked = recommend_songs(user_prefs, songs, k=2)
    assert ranked[0][0]["title"] == "Allowed Rock"
    assert "excluded genre" in ranked[1][2]


def test_zero_tolerance_uses_floor_instead_of_hard_zero_for_near_match():
    song = {
        "id": 1,
        "title": "Near Energy",
        "artist": "A",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.52,
        "tempo_bpm": 120,
        "valence": 0.50,
        "danceability": 0.50,
        "acousticness": 0.50,
    }
    user_prefs = {
        "weighting_scheme": "balanced",
        "target_energy": 0.50,
        "energy_tolerance": 0.0,
    }

    score, reasons = score_song(user_prefs, song)
    assert score > 0.0
    assert any("energy proximity" in r for r in reasons)


def test_novelty_bonus_only_applies_for_off_profile_song():
    on_profile = {
        "id": 1,
        "title": "On Profile",
        "artist": "A",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.50,
        "tempo_bpm": 110,
        "valence": 0.50,
        "danceability": 0.60,
        "acousticness": 0.40,
    }
    off_profile = {
        "id": 2,
        "title": "Off Profile",
        "artist": "B",
        "genre": "rock",
        "mood": "moody",
        "energy": 0.50,
        "tempo_bpm": 110,
        "valence": 0.50,
        "danceability": 0.60,
        "acousticness": 0.40,
    }
    user_prefs = {
        "weighting_scheme": "exploratory",
        "preferred_genres": {"pop": 1.0},
        "favorite_moods": {"happy": 1.0},
        "novelty_preference": 1.0,
    }

    _, on_reasons = score_song(user_prefs, on_profile)
    _, off_reasons = score_song(user_prefs, off_profile)
    assert all("novelty bonus" not in r for r in on_reasons)
    assert any("novelty bonus" in r for r in off_reasons)


def test_diversity_boost_changes_selected_scores():
    songs = [
        {
            "id": 1,
            "title": "Pop One",
            "artist": "A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "tempo_bpm": 120,
            "valence": 0.70,
            "danceability": 0.80,
            "acousticness": 0.20,
        },
        {
            "id": 2,
            "title": "Rock Two",
            "artist": "B",
            "genre": "rock",
            "mood": "happy",
            "energy": 0.79,
            "tempo_bpm": 119,
            "valence": 0.69,
            "danceability": 0.79,
            "acousticness": 0.21,
        },
    ]
    user_base = {
        "weighting_scheme": "balanced",
        "favorite_moods": {"happy": 1.0},
        "target_energy": 0.80,
    }

    ranked_no_boost = recommend_songs({**user_base, "diversity_boost": 0.0}, songs, k=2)
    ranked_with_boost = recommend_songs({**user_base, "diversity_boost": 1.0}, songs, k=2)

    top_title_no_boost, top_score_no_boost, _ = ranked_no_boost[0]
    top_title_with_boost, top_score_with_boost, _ = ranked_with_boost[0]
    assert top_title_no_boost["title"] == top_title_with_boost["title"]
    assert top_score_with_boost > top_score_no_boost
