from typing import Optional, Generic, TypeVar, Dict, List, Any
import strawberry

from utils import get_movies
from schema import Movie, MovieResult


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of movies.")
    def search_movies(
        self, query: str, limit: int, cursor: Optional[str] = None
    ) -> MovieResult:
        return get_movies(query, limit, cursor)
