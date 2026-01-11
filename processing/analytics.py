"""
Movie Analytics Engine
----------------------
Provides high-level analytical functions for the movie dataset using Pandas.
Core features include popularity rankings, weighted rating calculations, 
and demographic trends.
"""
import pandas as pd
import logging
from typing import Optional
from api.core.config import settings

logger = logging.getLogger(__name__)

class MovieAnalytics:
    """
    Core analytics engine for processing cleaned movie data.

    This class provides a suite of analytics methods using Pandas to derive
    insights such as popularity rankings, yearly trends, and genre analysis.
    It uses lazy loading to ensure data is only read when an analytics method
    is called.

    Attributes:
        data_path (Path): Path to the cleaned CSV dataset.
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initializes the analytics engine.

        Args:
            data_path (Optional[str]): Custom path to the cleaned dataset. 
                                       Defaults to settings.CLEANED_DATA_PATH.
        """
        self.data_path = data_path or settings.CLEANED_DATA_PATH
        self._df = None

    @property
    def df(self) -> pd.DataFrame:
        """
        Provides access to the loaded DataFrame, triggering load if necessary.

        Returns:
            pd.DataFrame: The loaded cleaned dataset.
        """
        if self._df is None:
            self._load_data()
        return self._df

    def _load_data(self) -> None:
        """
        Loads the preprocessed dataset from the filesystem.

        Raises:
            FileNotFoundError: If the cleaned data file does not exist.
        """
        try:
            logger.info(f"Loading analytics data from {self.data_path}")
            self._df = pd.read_csv(self.data_path, parse_dates=["Release_Date"])
        except Exception as e:
            logger.error(f"Error loading cleaned data: {e}")
            raise FileNotFoundError(f"Cleaned data not found at {self.data_path}. Run preprocessing first.")

    def get_movies_per_year(self) -> pd.DataFrame:
        """
        Calculates the volume of movie releases aggregated by year.

        Returns:
            pd.DataFrame: DataFrame with columns ['Year', 'movie_count'].
        """
        df = self.df.copy()
        df["Year"] = df["Release_Date"].dt.year
        return (
            df.groupby("Year")["Title"]
            .nunique()
            .reset_index(name="movie_count")
            .sort_values("Year")
        )

    def get_average_rating_per_genre(self) -> pd.DataFrame:
        """
        Calculates the mean vote rating for each genre.

        Returns:
            pd.DataFrame: DataFrame with columns ['Genre', 'average_rating'].
        """
        return (
            self.df.groupby("Genre")["Vote_Average"]
            .mean()
            .round(2)
            .reset_index(name="average_rating")
            .sort_values("average_rating", ascending=False)
        )

    def get_top_popular_movies(self, limit: int = 10) -> pd.DataFrame:
        """
        Ranks movies by their raw popularity score.

        Args:
            limit (int): Number of top records to return. Defaults to 10.

        Returns:
            pd.DataFrame: Top N popular movies.
        """
        return (
            self.df.sort_values("Popularity", ascending=False)
            .drop_duplicates(subset=["Title"])
            .head(limit)[["Title", "Popularity", "Vote_Average", "Vote_Count"]]
            .reset_index(drop=True)
        )

    @staticmethod
    def calculate_weighted_rating(df: pd.DataFrame) -> pd.Series:
        """
        Computes the IMDb-style Bayesian weighted rating.

        Formula: (v/(v+m)) * R + (m/(v+m)) * C

        Args:
            df (pd.DataFrame): DataFrame containing 'Vote_Count' and 'Vote_Average'.

        Returns:
            pd.Series: Computed weighted ratings.
        """
        v = df["Vote_Count"]
        R = df["Vote_Average"]
        m = df["Vote_Count"].quantile(0.70)
        C = df["Vote_Average"].mean()
        return (v / (v + m) * R) + (m / (v + m) * C)

    def get_top_rated_movies(self, limit: int = 10, min_votes: int = 500) -> pd.DataFrame:
        """
        Ranks movies by weighted rating, filtering out low-vote noise.

        Args:
            limit (int): Number of top records to return. Defaults to 10.
            min_votes (int): Minimum vote threshold for eligibility. Defaults to 500.

        Returns:
            pd.DataFrame: Top N rated movies by weighted score.
        """
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
        """
        Analyzes the distribution of movies across different languages.

        Returns:
            pd.DataFrame: DataFrame with columns ['Original_Language', 'movie_count'].
        """
        return (
            self.df.groupby("Original_Language")["Title"]
            .nunique()
            .reset_index(name="movie_count")
            .sort_values("movie_count", ascending=False)
        )