import pickle
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


# ---------------------------------------------------
# Recommend Movies
# ---------------------------------------------------

def recommend(movie_name, n=10):
    """
    Returns top n movie recommendations.
    """

    movie_name = movie_name.strip()

    if movie_name not in indices:
        return None

    idx = indices[movie_name]

    similarity_scores = cosine_similarity(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    similar_movies = similarity_scores.argsort()[::-1][1:n+1]

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
    """
    Returns closest matching movie names.
    """

    return get_close_matches(
        movie_name,
        list(indices.keys()),
        n=n,
        cutoff=0.5
    )


# ---------------------------------------------------
# Check Movie Exists
# ---------------------------------------------------

def movie_exists(movie_name):
    return movie_name in indices


# ---------------------------------------------------
# Movie Details
# ---------------------------------------------------

def get_movie_details(movie_name):

    if movie_name not in indices:
        return None

    movie = df[df["title"] == movie_name]

    if movie.empty:
        return None

    return movie.iloc[0]


# ---------------------------------------------------
# All Movie Titles
# ---------------------------------------------------

def get_all_titles():
    return sorted(df["title"].tolist())