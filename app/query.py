from typing import Optional, Generic, TypeVar, Dict, List, Any
import strawberry

from utils import get_movies
from schema import Movie, MovieConnection


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of movies.")
    def search_movies(
        self, query: str, first: int = 5, after: Optional[str] = None
    ) -> MovieConnection:
        return get_movies(query, first, after)
