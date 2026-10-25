import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.sparse import hstack


df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")

print(df.shape)
print(df.head(3))
print(df.isnull().sum())

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

G = MultiLabelBinarizer().fit_transform(df["genres"].str.split("|"))
hybrid = hstack([tfidf_matrix, G * 0.5])

print(tfidf_matrix.shape)

sim_matrix = cosine_similarity(hybrid)

def recommend(title, top_n=5, genre=None):
    match = df[df["title"].str.lower() == title.lower()]

    if match.empty:
        return None

    idx = match.index[0]
    scores = sorted(enumerate(sim_matrix[idx]), key=lambda x: x[1], reverse=True)

    results = []

    for i, s in scores:
        if i == idx:
            continue

        row = df.iloc[i]
        if genre and genre.lower() not in row["genres"].lower().split("|"):
            continue

        results.append({
            "title": row["title"],
            "genre": row["genres"],
            "rating": round(float(row["rating"]), 1),
            "score": round(float(s), 3),
        })
        if len(results) >= top_n:
            break

    return results