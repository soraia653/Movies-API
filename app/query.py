from typing import Optional

import strawberry

from app.schema import MovieConnection
from app.utils import get_movies


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of movies.")
    def search_movies(
        self, query: str, first: int = 5, after: Optional[str] = None
    ) -> MovieConnection:
        return get_movies(query, first, after)
