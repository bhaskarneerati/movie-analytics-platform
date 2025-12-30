from fastapi import APIRouter, Query, HTTPException
from typing import List

from processing.analytics import (
    top_movies_by_popularity,
    top_movies_by_weighted_rating,
    average_rating_per_genre,
    movies_released_per_year,
    movies_by_language,
)

from api.schemas import (
    TopPopularMoviesResponse,
    TopRatedMoviesResponse,
    MoviesByGenreResponse,
    MoviesPerYearResponse,
    MoviesByLanguageResponse,
)

router = APIRouter(prefix="/movies", tags=["Movies Analytics"])


# -------------------------------------------------------------------
# Popular Movies
# -------------------------------------------------------------------

@router.get(
    "/most-popular",
    response_model=TopPopularMoviesResponse
)
def get_most_popular_movies(
    limit: int = Query(10, ge=1, le=50)
):
    try:
        df = top_movies_by_popularity(limit)
        results = df.rename(columns={
            "Title": "title",
            "Popularity": "popularity",
            "Vote_Average": "vote_average",
            "Vote_Count": "vote_count",
        }).to_dict(orient="records")

        return {"results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# -------------------------------------------------------------------
# Top Rated Movies (Weighted)
# -------------------------------------------------------------------

@router.get(
    "/top-rated",
    response_model=TopRatedMoviesResponse
)
def get_top_rated_movies(
    limit: int = Query(10, ge=1, le=50),
    min_votes: int = Query(500, ge=0)
):
    try:
        df = top_movies_by_weighted_rating(
            limit=limit,
            min_votes=min_votes
        )

        results = df.rename(columns={
            "Title": "title",
            "Weighted_Rating": "weighted_rating",
            "Vote_Average": "vote_average",
            "Vote_Count": "vote_count",
        }).to_dict(orient="records")

        return {"results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# -------------------------------------------------------------------
# Genre Analytics
# -------------------------------------------------------------------

@router.get(
    "/by-genre",
    response_model=MoviesByGenreResponse
)
def get_movies_by_genre():
    try:
        df = average_rating_per_genre()
        results = df.rename(columns={
            "Genre": "genre",
            "average_rating": "average_rating",
        }).to_dict(orient="records")

        return {"results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# -------------------------------------------------------------------
# Yearly Trends
# -------------------------------------------------------------------

@router.get(
    "/yearly-trends",
    response_model=MoviesPerYearResponse
)
def get_yearly_trends():
    try:
        df = movies_released_per_year()
        results = df.rename(columns={
            "Year": "year",
            "movie_count": "movie_count",
        }).to_dict(orient="records")

        return {"results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# -------------------------------------------------------------------
# Language Distribution
# -------------------------------------------------------------------

@router.get(
    "/language-stats",
    response_model=MoviesByLanguageResponse
)
def get_language_stats():
    try:
        df = movies_by_language()
        results = df.rename(columns={
            "Original_Language": "language",
            "movie_count": "movie_count",
        }).to_dict(orient="records")

        return {"results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))