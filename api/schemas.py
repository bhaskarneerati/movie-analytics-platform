from pydantic import BaseModel
from typing import List


# -------------------------------------------------------------------
# Movie Ranking Schemas
# -------------------------------------------------------------------

class TopPopularMovie(BaseModel):
    title: str
    popularity: float
    vote_average: float
    vote_count: int


class TopRatedMovie(BaseModel):
    title: str
    weighted_rating: float
    vote_average: float
    vote_count: int


# -------------------------------------------------------------------
# Aggregation Schemas
# -------------------------------------------------------------------

class MoviesByGenre(BaseModel):
    genre: str
    average_rating: float


class MoviesPerYear(BaseModel):
    year: int
    movie_count: int


class MoviesByLanguage(BaseModel):
    language: str
    movie_count: int


# -------------------------------------------------------------------
# Wrapper Response Schemas
# -------------------------------------------------------------------

class TopPopularMoviesResponse(BaseModel):
    results: List[TopPopularMovie]


class TopRatedMoviesResponse(BaseModel):
    results: List[TopRatedMovie]


class MoviesByGenreResponse(BaseModel):
    results: List[MoviesByGenre]


class MoviesPerYearResponse(BaseModel):
    results: List[MoviesPerYear]


class MoviesByLanguageResponse(BaseModel):
    results: List[MoviesByLanguage]