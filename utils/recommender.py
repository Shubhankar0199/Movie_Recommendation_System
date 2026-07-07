import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

with open("data/df.pkl", "rb") as f:
    df = pickle.load(f)

with open("data/indices.pkl", "rb") as f:
    indices = pickle.load(f)

with open("data/tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix = pickle.load(f)

# Make sure popularity is numeric
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")

# ---------------------------------------------------
# Recommend Movies
# ---------------------------------------------------

def recommend(movie_name, n=10):
    """
    Returns top n movie recommendations.
    Automatically handles duplicate movie titles.
    """

    movie_name = movie_name.strip()

    # Find all movies with the same title (case-insensitive)
    matches = df[
        df["title"].str.lower() == movie_name.lower()
    ]

    if matches.empty:
        return None

    # If there are duplicate titles, choose the most popular one
    idx = (
        matches
        .sort_values("popularity", ascending=False)
        .index[0]
    )

    similarity_scores = cosine_similarity(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    similar_movies = similarity_scores.argsort()[::-1]

    # Remove the selected movie itself
    similar_movies = similar_movies[similar_movies != idx]

    # Keep only valid indices
    similar_movies = [
        i for i in similar_movies
        if 0 <= i < len(df)
    ]

    similar_movies = similar_movies[:n]

    recommendations = df.iloc[similar_movies][
        [
            "title",
            "genres",
            "tagline",
            "vote_average",
            "popularity",
            "overview"
        ]
    ]

    return recommendations.reset_index(drop=True)

# ---------------------------------------------------
# Movie Suggestions
# ---------------------------------------------------

def get_movie_suggestions(movie_name, n=5):

    titles = df["title"].drop_duplicates().tolist()

    return get_close_matches(
        movie_name,
        titles,
        n=n,
        cutoff=0.5
    )

# ---------------------------------------------------
# Check Movie Exists
# ---------------------------------------------------

def movie_exists(movie_name):

    return (
        df["title"]
        .str.lower()
        .eq(movie_name.lower())
        .any()
    )

# ---------------------------------------------------
# Movie Details
# ---------------------------------------------------

def get_movie_details(movie_name):

    matches = df[
        df["title"].str.lower() == movie_name.lower()
    ]

    if matches.empty:
        return None

    movie = matches.sort_values(
        "popularity",
        ascending=False
    ).iloc[0]

    return movie

# ---------------------------------------------------
# All Movie Titles
# ---------------------------------------------------

def get_all_titles():

    return sorted(
        df["title"]
        .drop_duplicates()
        .tolist()
    )