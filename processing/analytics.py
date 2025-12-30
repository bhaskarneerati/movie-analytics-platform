import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DATA_PATH = BASE_DIR / "data" / "cleaned_movies.csv"


def load_cleaned_data() -> pd.DataFrame:
    """
    Load preprocessed movie dataset.
    """
    return pd.read_csv(CLEANED_DATA_PATH, parse_dates=["Release_Date"])


# -------------------------------------------------------------------
# Core Analytics Functions
# -------------------------------------------------------------------

def movies_released_per_year() -> pd.DataFrame:
    """
    Number of movies released per year.
    """
    df = load_cleaned_data()
    df["Year"] = df["Release_Date"].dt.year

    return (
        df.groupby("Year")["Title"]
        .nunique()
        .reset_index(name="movie_count")
        .sort_values("Year")
    )


def average_rating_per_genre() -> pd.DataFrame:
    """
    Average vote rating per genre.
    """
    df = load_cleaned_data()

    return (
        df.groupby("Genre")["Vote_Average"]
        .mean()
        .round(2)
        .reset_index(name="average_rating")
        .sort_values("average_rating", ascending=False)
    )


def top_movies_by_popularity(limit: int = 10) -> pd.DataFrame:
    """
    Top N movies ranked by popularity.
    """
    df = load_cleaned_data()

    return (
        df.sort_values("Popularity", ascending=False)
        .drop_duplicates(subset=["Title"])
        .head(limit)[
            ["Title", "Popularity", "Vote_Average", "Vote_Count"]
        ]
        .reset_index(drop=True)
    )


def calculate_weighted_rating(df: pd.DataFrame) -> pd.Series:
    """
    IMDb-style weighted rating.
    """
    v = df["Vote_Count"]
    R = df["Vote_Average"]

    m = df["Vote_Count"].quantile(0.70)
    C = df["Vote_Average"].mean()

    return (v / (v + m) * R) + (m / (v + m) * C)


def top_movies_by_weighted_rating(
    limit: int = 10,
    min_votes: int = 500
) -> pd.DataFrame:
    """
    Top N movies by weighted rating with vote threshold.
    """
    df = load_cleaned_data()
    df = df[df["Vote_Count"] >= min_votes]

    df["Weighted_Rating"] = calculate_weighted_rating(df)

    return (
        df.sort_values("Weighted_Rating", ascending=False)
        .drop_duplicates(subset=["Title"])
        .head(limit)[
            ["Title", "Weighted_Rating", "Vote_Average", "Vote_Count"]
        ]
        .round(2)
        .reset_index(drop=True)
    )


def movies_by_language() -> pd.DataFrame:
    """
    Movie distribution by original language.
    """
    df = load_cleaned_data()

    return (
        df.groupby("Original_Language")["Title"]
        .nunique()
        .reset_index(name="movie_count")
        .sort_values("movie_count", ascending=False)
    )