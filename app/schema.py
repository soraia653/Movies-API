import strawberry
from typing import List, Optional


# class represents a single movie
@strawberry.type
class Movie:
    Title: str = strawberry.field()
    Year: str = strawberry.field()
    imdbID: str = strawberry.field()
    Type: str = strawberry.field()
    Poster: str = strawberry.field()
    id: int = strawberry.field()


# class represents the results of a movie search:
@strawberry.type
class MovieResult:
    total_results: int
    movies: List[Movie]
