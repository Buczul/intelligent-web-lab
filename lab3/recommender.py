import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("ratings.csv")

matrix = df.pivot_table(index="user", columns="title", values="rating")

print(matrix.shape)

means = matrix.mean(axis=1)
centered = matrix.sub(means, axis=0).fillna(0)

sim = pd.DataFrame(cosine_similarity(centered), index=matrix.index, columns=matrix.index)

items = centered.T

sim_items = pd.DataFrame(cosine_similarity(items), index=items.index, columns=items.index)

def fallback(user, top_n=5):
    movie_means = df.groupby("title")["rating"].mean()

    rated = matrix.loc[user].notna()

    sorted_movie_means = movie_means.sort_values(ascending=False)[~rated][:top_n]

    return [
        {"title": t, "rate": round(float(r), 2)}
        for t, r in sorted_movie_means.items()
    ]

def recommend(user, top_n=5, k=3):
    if user not in matrix.index:
        return None

    rated_movies = matrix.loc[user].notna().sum()
    if rated_movies <= 1: return fallback(user)

    neighbors = sim[user].drop(user).sort_values(ascending=False).head(k)

    scores = {}
    for movie in matrix.columns:
        if not pd.isna(matrix.loc[user, movie]):
            continue

        num, den = 0.0, 0.0
        for other, w in neighbors.items():
            r = matrix.loc[other, movie]
            if not pd.isna(r):
                num += w * (r - means[other])
                den += abs(w)

        if den > 0:
            scores[movie] = max(1.0, min(5.0, means[user] + num / den))

    best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return [{"title": t,
             "predicted": round(float(s), 2),
             "because": [o for o, weight in neighbors.items()
                         if weight != 0 and not pd.isna(matrix.loc[o, t])]
             } for t, s in best]