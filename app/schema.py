from typing import List, Optional, Dict, Any
import strawberry


@strawberry.type
class PageInfo:
    """Pagination metadata."""

    next_cursor: Optional[str] = strawberry.field()


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


@strawberry.type
class MovieResult:
    """Class represents the results of a movie search."""

    total_results: int
    movies: List[Movie]
    page_info: PageInfo = strawberry.field()
