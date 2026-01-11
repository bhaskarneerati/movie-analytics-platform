import pandas as pd
import logging
from typing import Optional
from api.core.config import settings

logger = logging.getLogger(__name__)

class MovieAnalytics:
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or settings.CLEANED_DATA_PATH
        self._df = None

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            self._load_data()
        return self._df

    def _load_data(self) -> None:
        """Loads preprocessed movie dataset."""
        try:
            logger.info(f"Loading analytics data from {self.data_path}")
            self._df = pd.read_csv(self.data_path, parse_dates=["Release_Date"])
        except Exception as e:
            logger.error(f"Error loading cleaned data: {e}")
            raise FileNotFoundError(f"Cleaned data not found at {self.data_path}. Run preprocessing first.")

    def get_movies_per_year(self) -> pd.DataFrame:
        """Number of movies released per year."""
        df = self.df.copy()
        df["Year"] = df["Release_Date"].dt.year
        return (
            df.groupby("Year")["Title"]
            .nunique()
            .reset_index(name="movie_count")
            .sort_values("Year")
        )

    def get_average_rating_per_genre(self) -> pd.DataFrame:
        """Average vote rating per genre."""
        return (
            self.df.groupby("Genre")["Vote_Average"]
            .mean()
            .round(2)
            .reset_index(name="average_rating")
            .sort_values("average_rating", ascending=False)
        )

    def get_top_popular_movies(self, limit: int = 10) -> pd.DataFrame:
        """Top N movies ranked by popularity."""
        return (
            self.df.sort_values("Popularity", ascending=False)
            .drop_duplicates(subset=["Title"])
            .head(limit)[["Title", "Popularity", "Vote_Average", "Vote_Count"]]
            .reset_index(drop=True)
        )

    @staticmethod
    def calculate_weighted_rating(df: pd.DataFrame) -> pd.Series:
        """IMDb-style weighted rating formula."""
        v = df["Vote_Count"]
        R = df["Vote_Average"]
        m = df["Vote_Count"].quantile(0.70)
        C = df["Vote_Average"].mean()
        return (v / (v + m) * R) + (m / (v + m) * C)

    def get_top_rated_movies(self, limit: int = 10, min_votes: int = 500) -> pd.DataFrame:
        """Top N movies by weighted rating with vote threshold."""
        df_filtered = self.df[self.df["Vote_Count"] >= min_votes].copy()
        if df_filtered.empty:
            return pd.DataFrame(columns=["Title", "Weighted_Rating", "Vote_Average", "Vote_Count"])
            
        df_filtered["Weighted_Rating"] = self.calculate_weighted_rating(df_filtered)
        return (
            df_filtered.sort_values("Weighted_Rating", ascending=False)
            .drop_duplicates(subset=["Title"])
            .head(limit)[["Title", "Weighted_Rating", "Vote_Average", "Vote_Count"]]
            .round(2)
            .reset_index(drop=True)
        )

    def get_language_diversity(self) -> pd.DataFrame:
        """Movie distribution by original language."""
        return (
            self.df.groupby("Original_Language")["Title"]
            .nunique()
            .reset_index(name="movie_count")
            .sort_values("movie_count", ascending=False)
        )