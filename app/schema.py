from typing import List, Optional, Dict, Any
import strawberry


@strawberry.type
class PageInfo:
    """Pagination metadata."""

    start_cursor: Optional[str] = strawberry.field()
    end_cursor: Optional[str] = strawberry.field()
    has_next_page: bool = strawberry.field()
    has_previous_page: bool = strawberry.field()


@strawberry.type
class Movie:
    """Class that represents a single movie."""

    Title: str = strawberry.field()
    Year: str = strawberry.field()
    imdbID: str = strawberry.field()
    Type: str = strawberry.field()
    Poster: str = strawberry.field()
    id: int = strawberry.field()

    @staticmethod
    def from_row(row: Dict[str, Any], movie_id: int) -> "Movie":
        """Transforms row data into Movie object."""
        return Movie(
            Title=row["Title"],
            Year=row["Year"],
            imdbID=row["imdbID"],
            Type=row["Type"],
            Poster=row["Poster"],
            id=movie_id,
        )


# @strawberry.type
# class MovieResult:
#     """Class represents the results of a movie search."""

#     total_results: int
#     movies: List[Movie]
#     page_info: PageInfo = strawberry.field()


@strawberry.type
class MovieEdge:
    """Each edge contains it's own cursor and item (movie)."""

    node: Movie = strawberry.field()
    cursor: str = strawberry.field()


@strawberry.type
class MovieConnection:
    """Class represents the results of a movie search."""

    total_results: int
    movies: List[MovieEdge] = strawberry.field()
    page_info: "PageInfo" = strawberry.field()
