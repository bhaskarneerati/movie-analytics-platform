"""
Movie Analytics Routes
----------------------
Defines the RESTful API endpoints for movie analytics. 
Integrates with the analytics engine via dependency injection.
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Any
import logging

from processing.analytics import MovieAnalytics
from api.schemas import (
    TopPopularMoviesResponse,
    TopRatedMoviesResponse,
    MoviesByGenreResponse,
    MoviesPerYearResponse,
    MoviesByLanguageResponse,
)

router = APIRouter(prefix="/movies", tags=["Analytics"])
logger = logging.getLogger(__name__)

# Dependency to get analytics instance
def get_analytics():
    """
    Dependency provider for the MovieAnalytics engine.

    Ensures the underlying data file is accessible before processing requests.

    Returns:
        MovieAnalytics: An instance of the analytics engine.

    Raises:
        HTTPException: 503 error if the cleaned data file is missing.
    """
    try:
        return MovieAnalytics()
    except FileNotFoundError as e:
        logger.error(f"Data dependency error: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Data layer not initialized. Please run preprocessing."
        )

@router.get("/most-popular", response_model=TopPopularMoviesResponse)
def get_most_popular_movies(
    limit: int = Query(10, ge=1, le=50),
    analytics: MovieAnalytics = Depends(get_analytics)
):
    """
    Retrieves the top N movies based on their raw popularity score.

    Args:
        limit (int): Max number of movies to return (1-50). Defaults to 10.
        analytics (MovieAnalytics): Injected analytics engine instance.

    Returns:
        dict: Wrapped list of popular movies.
    """
    try:
        df = analytics.get_top_popular_movies(limit)
        results = df.rename(columns={
            "Title": "title",
            "Popularity": "popularity",
            "Vote_Average": "vote_average",
            "Vote_Count": "vote_count",
        }).to_dict(orient="records")
        return {"results": results}
    except Exception as e:
        logger.exception("Error fetching popular movies")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/top-rated", response_model=TopRatedMoviesResponse)
def get_top_rated_movies(
    limit: int = Query(10, ge=1, le=50),
    min_votes: int = Query(500, ge=0),
    analytics: MovieAnalytics = Depends(get_analytics)
):
    """
    Retrieves top rated movies using a Bayesian weighted rating formula.

    This endpoint filters out movies with low vote counts to ensure ranking credibility.

    Args:
        limit (int): Max number of movies to return (1-50). Defaults to 10.
        min_votes (int): Minimum vote threshold. Defaults to 500.
        analytics (MovieAnalytics): Injected analytics engine instance.

    Returns:
        dict: Wrapped list of top-rated movies.
    """
    try:
        df = analytics.get_top_rated_movies(limit, min_votes)
        results = df.rename(columns={
            "Title": "title",
            "Weighted_Rating": "weighted_rating",
            "Vote_Average": "vote_average",
            "Vote_Count": "vote_count",
        }).to_dict(orient="records")
        return {"results": results}
    except Exception as e:
        logger.exception("Error fetching top rated movies")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/by-genre", response_model=MoviesByGenreResponse)
def get_movies_by_genre(analytics: MovieAnalytics = Depends(get_analytics)):
    """
    Calculates the average global rating for every movie genre.

    Args:
        analytics (MovieAnalytics): Injected analytics engine instance.

    Returns:
        dict: Wrapped list of genre-based performance stats.
    """
    try:
        df = analytics.get_average_rating_per_genre()
        results = df.rename(columns={
            "Genre": "genre",
            "average_rating": "average_rating",
        }).to_dict(orient="records")
        return {"results": results}
    except Exception as e:
        logger.exception("Error fetching genre stats")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/yearly-trends", response_model=MoviesPerYearResponse)
def get_yearly_trends(analytics: MovieAnalytics = Depends(get_analytics)):
    """
    Retrieves historical movie release volume aggregated by year.

    Args:
        analytics (MovieAnalytics): Injected analytics engine instance.

    Returns:
        dict: Wrapped list of yearly counts.
    """
    try:
        df = analytics.get_movies_per_year()
        results = df.rename(columns={
            "Year": "year",
            "movie_count": "movie_count",
        }).to_dict(orient="records")
        return {"results": results}
    except Exception as e:
        logger.exception("Error fetching yearly trends")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/language-stats", response_model=MoviesByLanguageResponse)
def get_language_stats(analytics: MovieAnalytics = Depends(get_analytics)):
    """
    Calculates movie distribution and volume by original language of production.

    Args:
        analytics (MovieAnalytics): Injected analytics engine instance.

    Returns:
        dict: Wrapped list of language statistics.
    """
    try:
        df = analytics.get_language_diversity()
        results = df.rename(columns={
            "Original_Language": "language",
            "movie_count": "movie_count",
        }).to_dict(orient="records")
        return {"results": results}
    except Exception as e:
        logger.exception("Error fetching language stats")
        raise HTTPException(status_code=500, detail="Internal server error")