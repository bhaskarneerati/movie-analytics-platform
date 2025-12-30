import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw_movies.csv"
CLEANED_DATA_PATH = BASE_DIR / "data" / "cleaned_movies.csv"


# def load_raw_data() -> pd.DataFrame:
#     """
#     Load raw movie dataset from CSV.
#     """
#     return pd.read_csv(RAW_DATA_PATH)

def load_raw_data() -> pd.DataFrame:
    """
    Load raw movie dataset from CSV.
    Uses Python engine for robustness against long text fields.
    """
    return pd.read_csv(
        RAW_DATA_PATH,
        engine="python",
        quotechar='"',
        encoding="utf-8",
    )


# def clean_movies_data(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Perform data cleaning and normalization.
#     """

#     # --- Date handling ---
#     df["Release_Date"] = pd.to_datetime(df["Release_Date"], errors="coerce")
#     df = df.dropna(subset=["Release_Date"])

#     # --- Numeric coercion ---
#     numeric_columns = ["Popularity", "Vote_Count", "Vote_Average"]
#     for col in numeric_columns:
#         df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

#     # --- Categorical cleanup ---
#     df["Original_Language"] = (
#         df["Original_Language"]
#         .fillna("unknown")
#         .str.lower()
#         .str.strip()
#     )

#     df["Genre"] = (
#         df["Genre"]
#         .fillna("Unknown")
#         .astype(str)
#         .str.split(",")
#     )

#     # Normalize whitespace in genre list
#     df["Genre"] = df["Genre"].apply(lambda genres: [g.strip() for g in genres])

#     # --- Explode genres ---
#     df = df.explode("Genre")

#     # --- Final safety cleanup ---
#     df["Genre"] = df["Genre"].replace("", "Unknown")

#     # --- Sorting for determinism ---
#     df = df.sort_values(by=["Release_Date", "Title"]).reset_index(drop=True)

#     return df

def clean_movies_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform data cleaning and normalization.
    """

    # --- Date handling ---
    df = df.copy()
    df.loc[:, "Release_Date"] = pd.to_datetime(df["Release_Date"], errors="coerce")
    df = df.dropna(subset=["Release_Date"]).copy()

    # --- Numeric coercion ---
    numeric_columns = ["Popularity", "Vote_Count", "Vote_Average"]
    for col in numeric_columns:
        df.loc[:, col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # --- Categorical cleanup ---
    df.loc[:, "Original_Language"] = (
        df["Original_Language"]
        .fillna("unknown")
        .str.lower()
        .str.strip()
    )

    # --- Genre normalization ---
    df.loc[:, "Genre"] = (
        df["Genre"]
        .fillna("Unknown")
        .astype(str)
        .str.split(",")
    )

    df.loc[:, "Genre"] = df["Genre"].apply(
        lambda genres: [g.strip() for g in genres]
    )

    # --- Explode genres ---
    df = df.explode("Genre").copy()

    # --- Final safety cleanup ---
    df.loc[:, "Genre"] = df["Genre"].replace("", "Unknown")

    # --- Sorting for determinism ---
    df = df.sort_values(by=["Release_Date", "Title"]).reset_index(drop=True)

    return df

def save_cleaned_data(df: pd.DataFrame) -> None:
    """
    Persist cleaned dataset to disk.
    """
    df.to_csv(CLEANED_DATA_PATH, index=False)


def run_preprocessing_pipeline() -> None:
    """
    Full preprocessing pipeline.
    """
    raw_df = load_raw_data()
    cleaned_df = clean_movies_data(raw_df)
    save_cleaned_data(cleaned_df)


if __name__ == "__main__":
    run_preprocessing_pipeline()