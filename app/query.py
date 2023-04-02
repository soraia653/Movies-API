import strawberry
from typing import Optional
from app.utils import get_movies
from app.schema import MovieConnection


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of movies.")
    def search_movies(
        self, query: str, first: int = 5, after: Optional[str] = None
    ) -> MovieConnection:
        return get_movies(query, first, after)
