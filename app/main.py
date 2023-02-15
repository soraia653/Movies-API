# required libraries
import strawberry
from typing import Optional, Generic, TypeVar, Dict, List, Any
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import requests

OMDB_URL = "http://www.omdbapi.com/?apikey=c05820ad&s={}"

# get filtered movie data from OMDB API
def get_movie_data(s):
  movie_data = requests.get(OMDB_URL.format(s)).json()
  return movie_data

@strawberry.type
class Movie:
    Title: str = strawberry.field()
    Year: str = strawberry.field()
    imdbID: str = strawberry.field()
    Type: str = strawberry.field()
    Poster: str = strawberry.field()

    @staticmethod
    def from_row(row: Dict[str, Any]):
        return Movie(
            Title=row['Title'],
            Year=row['Year'],
            imdbID=row['imdbID'],
            Type=row['Type'],
            Poster=row['Poster']
        )

# create pagination -> represents one piece of paginated items.
GenericType = TypeVar("GenericType")

@strawberry.type
class SinglePage(List[GenericType]):
    items: List[GenericType] = strawberry.field(
        description="List of all movies in this paginated window."
    )
    total_items_count: int = strawberry.field(
        description="Total number of items in the filtered dataset."
    )

# define get_single_page function
def get_single_page(dataset: List[GenericType], ItemType: type, order_by: str, limit: int):
   
   if limit <= 0 or limit > 100:
      raise Exception(f"Limit ({limit}) must be between 0 and 100.")
   
   # sort data based on given field
   dataset.sort(key=lambda x: x[order_by])

  # get total count of items
   total_items_count = len(dataset)

   items = dataset[:limit]
   items = [ItemType.from_row(x) for x in items]

   return SinglePage(
      items=items,
      total_items_count=total_items_count
   )

# query definition
@strawberry.type
class Query:
   
    # resolvers as methods
    @strawberry.field(description = "Get a list of movies.")
    def get_movie(self,
                  order_by: str,
                  limit: int,
                  title: str
                  ) -> SinglePage[Movie]:

        if title is not None:
          movie_data = get_movie_data(title)['Search']
        
          return get_single_page(
             dataset=movie_data,
             ItemType=Movie,
             order_by=order_by,
             limit=limit
          )

app = FastAPI()

# URL ROUTES
schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)