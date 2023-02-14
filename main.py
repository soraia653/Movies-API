# required libraries
import strawberry
from typing import Optional, Generic, TypeVar
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import requests

from base64 import b64encode, b64decode
from helper_functions import *

OMDB_URL = "http://www.omdbapi.com/?apikey=c05820ad&s={}"

# apply pagination
GenericType = TypeVar("GenericType")

@strawberry.type
class Connection(Generic[GenericType]):
    page_info: "PageInfo" = strawberry.field()
    edges: list["Edge[GenericType]"] = strawberry.field()

@strawberry.type
class PageInfo:
  has_next_page: bool = strawberry.field()
  has_previous_page: bool = strawberry.field()
  start_cursor: Optional[str] = strawberry.field()
  end_cursor: Optional[str] = strawberry.field()

@strawberry.type
class Edge(Generic[GenericType]):
  node: GenericType = strawberry.field()
  cursor: str = strawberry.field()

@strawberry.type
class Movie:
    name: str
    year: str
    rated: str
    released: str
    runtime: str
    genre: str
    director: str
    writer: str
    actors: str
    plot: str
    imdbRating: float
    type: str

@strawberry.type
class Query:
   
   # resolvers as methods
   @strawberry.field
   def movie(self, MovieName: str, first: int = 2, after: Optional[str] = None) -> Connection[Movie]:
      
      # complete from here https://strawberry.rocks/docs/guides/pagination/connections
      
      if MovieName is strawberry.UNSET:
         return "Name was not set."
      
      if MovieName is not None:
        movie_data = get_movie_data(MovieName)
        movie_data = movie_data['Search']

        return [
           Movie(
            name = movie['Title'],
            year = movie['Year'],
            rated = movie['Rated'],
            released = movie['Released'],
            runtime = movie['Runtime'],
            genre = movie['Genre'],
            director = movie['Director'],
            writer = movie['Writer'],
            actors = movie['Actors'],
            plot = movie['Plot'],
            imdbRating = movie['imdbRating'],
            type = movie['Type']
          )
          for movie in movie_data
        ]

app = FastAPI()

# URL ROUTES
@app.get("/")
async def index():
  return {"message": "Greetings!"}

@app.get("/movie/{movie_name}")
async def get_movie(movie_name):
  movie = get_movie_data(movie_name)
  return movie

schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)