"""
Data Preprocessing Module
-------------------------
Handles the transformation of raw movie CSV data into a cleaned, 
analytics-ready format. Includes logic for date parsing, numeric 
normalization, and multi-genre explosion.
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Optional
from api.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MovieDataPreprocessor:
    """
    Handles the end-to-end data engineering pipeline for movie datasets.

    This class provides methods to load raw CSV data, perform cleaning and 
    normalization (including genre explosion), and persist the cleaned data 
    for downstream analytics.

    Attributes:
        raw_path (Path): Path to the source raw CSV file.
        output_path (Path): Path where the cleaned CSV will be saved.
    """

    def __init__(self, raw_path: Path, output_path: Path):
        """
        Initializes the preprocessor with source and destination paths.

        Args:
            raw_path (Path): Absolute path to the raw input data.
            output_path (Path): Absolute path for the cleaned output data.
        """
        self.raw_path = raw_path
        self.output_path = output_path

    def load_data(self) -> pd.DataFrame:
        """
        Loads the raw movie dataset from the local filesystem.

        Uses the Python engine for robust parsing of long text fields (e.g., overviews).

        Returns:
            pd.DataFrame: The raw dataset loaded as a Pandas DataFrame.

        Raises:
            FileNotFoundError: If no file exists at the specified raw_path.
        """
        if not self.raw_path.exists():
            logger.error(f"Raw data file not found at {self.raw_path}")
            raise FileNotFoundError(f"Raw data file not found at {self.raw_path}")
        
        logger.info(f"Loading raw data from {self.raw_path}")
        return pd.read_csv(
            self.raw_path,
            engine="python",
            quotechar='"',
            encoding="utf-8",
        )

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes cleaning, type coercion, and normalization logic.

        Operations include:
        - Date parsing and handling missing dates.
        - Numeric coercion for popularity and vote metrics.
        - Normalizing categorical fields (Language, Genre).
        - Exploding multi-valued genres into individual rows.
        - Sorting records for deterministic output.

        Args:
            df (pd.DataFrame): The raw input DataFrame.

        Returns:
            pd.DataFrame: A cleaned and normalized DataFrame.
        """
        logger.info("Starting data cleaning process...")
        df = df.copy()

        # Date handling
        df["Release_Date"] = pd.to_datetime(df["Release_Date"], errors="coerce")
        initial_count = len(df)
        df = df.dropna(subset=["Release_Date"]).copy()
        logger.info(f"Dropped {initial_count - len(df)} rows with invalid dates")

        # Numeric coercion
        numeric_cols = ["Popularity", "Vote_Count", "Vote_Average"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Categorical cleanup
        df["Original_Language"] = (
            df["Original_Language"]
            .fillna("unknown")
            .astype(str)
            .str.lower()
            .str.strip()
        )

        # Genre normalization
        df["Genre"] = (
            df["Genre"]
            .fillna("Unknown")
            .astype(str)
            .str.split(",")
        )
        df["Genre"] = df["Genre"].apply(lambda genres: [g.strip() for g in genres])

        # Explode genres
        df = df.explode("Genre").copy()
        df["Genre"] = df["Genre"].replace("", "Unknown")

        # Sorting
        df = df.sort_values(by=["Release_Date", "Title"]).reset_index(drop=True)
        
        logger.info(f"Data cleaning complete. Final record count (exploded): {len(df)}")
        return df

    def save_data(self, df: pd.DataFrame) -> None:
        """
        Persists the processed DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The cleaned DataFrame to save.
        """
        logger.info(f"Saving cleaned data to {self.output_path}")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.output_path, index=False)

    def run(self) -> None:
        """
        Orchestrates the full preprocessing pipeline.

        Reads source -> Cleans -> Writes destination.
        """
        try:
            raw_df = self.load_data()
            cleaned_df = self.clean_data(raw_df)
            self.save_data(cleaned_df)
            logger.info("Pipeline executed successfully.")
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise

if __name__ == "__main__":
    preprocessor = MovieDataPreprocessor(
        raw_path=settings.RAW_DATA_PATH,
        output_path=settings.CLEANED_DATA_PATH
    )
    preprocessor.run()