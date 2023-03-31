# query definition
import strawberry
from typing import Optional, Generic, TypeVar, Dict, List, Any

from utils import get_movies
from schema import MovieResult


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of movies.")
    def search_movies(self, query: str) -> MovieResult:
        return get_movies(query)
