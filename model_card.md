# 🎧 Model Card: Music Recommender Simulation

## Model Name

MoodShift Recommender 1.0

---

## Goal / Task

This model suggests songs for a user profile.
It predicts which songs are the best top-k match.
It uses user taste and song audio features.

---

## Data Used

I used a small catalog of 100 songs.
Each song has genre, mood, energy, tempo, valence, danceability, and acousticness.
The data is balanced by label counts, but it is still small.
It does not include lyrics, language, culture, or listening history.

---

## Algorithm Summary

The model gives points for genre and mood matches.
Then it gives points for being close to target energy, tempo, valence, danceability, and acousticness.
It can also apply an excluded-genre penalty, a novelty bonus, and a diversity boost.
Songs are sorted by total score, then top-k is returned.

---

## Observed Behavior / Biases

One clear weakness is category over-anchoring.
Songs with strong genre or mood labels can win too often.
This can create a filter bubble and repetitive top results.
Contradictory profiles showed this most clearly in experiments.

---

## Evaluation Process

I tested seven profiles: high_energy_pop, chill_lofi, deep_intense_rock, conflict_energy_sad, self_contradict_exclude_only_genre, zero_tolerance_trap, novelty_max_no_prefs.
I compared top-5 outputs and checked if they made sense for each mood goal.
I also ran a weight-shift sensitivity experiment and a mitigation experiment.
The main surprise was that one upbeat pop song stayed near the top very often.

---

## Intended Use and Non-Intended Use

Intended use: classroom learning, model behavior analysis, and transparent recommendation demos.
Not intended use: real clinical, hiring, safety, or high-stakes personalization decisions.
Not intended use: production music recommendation for large and diverse user bases.

---

## Ideas for Improvement

1. Add state-aware profiles (for example calm mode vs courage mode).
2. Add richer features like instrument tags and lyric themes.
3. Improve diversity controls so repeated winners happen less often.

---

## Personal Reflection on Engineering Process

My biggest learning moment was seeing how one small scoring rule can change the whole ranking behavior. When I changed weights or tolerance logic, the top songs changed quickly, even though the code edit looked small. That taught me to treat recommender tuning like system design, not just parameter tweaking.

AI tools helped me move faster when drafting experiments, generating profile ideas, and summarizing results. But I still had to double-check outputs by running the code and reading actual score reasons. I learned that AI suggestions are useful starting points, not final truth.

I was surprised that a simple additive scoring algorithm could still feel like a real recommender. Even with basic rules, users can feel a song is "for them" when genre, mood, and energy line up. At the same time, the same simplicity can create bias, like repeated winners and filter-bubble patterns.

If I continue this project, I would try three next steps: add context-aware user states (calm mode vs courage mode), add richer music features (for example instrument tags), and test stronger diversity controls with clear tradeoff metrics.

