# required libraries
import strawberry
from typing import Optional, Generic, TypeVar, Dict, List, Any
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import requests
import os
from dotenv import load_dotenv
from base64 import b64encode, b64decode

# load environment variable
load_dotenv()

API_KEY = os.getenv('API_KEY')

OMDB_URL = "http://www.omdbapi.com/?apikey={}&s={}"

# get filtered movie data from OMDB API
def get_movie_data(s):
    movie_data = requests.get(OMDB_URL.format(API_KEY, s)).json()
    return movie_data

# encode / decode functions
def encode_user_cursor(id: int) -> str:
	return b64encode(f"movie:{id}".encode("ascii")).decode("ascii")

def decode_user_cursor(cursor: str) -> int:
	cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
	return int(cursor_data.split(":")[1])

GenericType = TypeVar("GenericType")

@strawberry.type
class Connection(Generic[GenericType]):
    page_info: "PageInfo" = strawberry.field(
		description="Information to aid in pagination."
    )

    edges: list["Edge[GenericType]"] = strawberry.field(
    	description="A list of edges in this connection."
    )


@strawberry.type
class PageInfo:
    has_next_page: bool = strawberry.field(
    	description="When paginating forwards, are there more items?"
    )


    has_previous_page: bool = strawberry.field(
    	description="When paginating backwards, are there more items?"
    )


    start_cursor: Optional[str] = strawberry.field(
    	description="When paginating backwards, the cursor to continue."
    )


    end_cursor: Optional[str] = strawberry.field(
		description="When paginating forwards, the cursor to continue."
    )

@strawberry.type
class Edge(Generic[GenericType]):
    node: GenericType = strawberry.field(
    	description="The item at the end of the edge."
    )


    cursor: str = strawberry.field(
    	description="A cursor for use in pagination."
    )

@strawberry.type
class Movie:
	Title: str = strawberry.field()
	Year: str = strawberry.field()
	imdbID: str = strawberry.field()
	Type: str = strawberry.field()
	Poster: str = strawberry.field()
	id: int = strawberry.field()

	@staticmethod
	def from_row(row: Dict[str, Any]):
		return Movie(
            Title=row['Title'],
            Year=row['Year'],
            imdbID=row['imdbID'],
            Type=row['Type'],
            Poster=row['Poster'],
            id=row['id']
        )


# query definition
@strawberry.type
class Query:
	# resolvers as methods
	@strawberry.field(description = "Get a list of movies.")
	def get_movie(self, title: str, first: int = 2, after: Optional[str] = None) -> Connection[Movie]:
		
		if after is not None:
			movie_id = decode_user_cursor(cursor=after)
		else:
			movie_id = 0

		if title is not None:
			movie_data = get_movie_data(title)['Search']

			# generate ID for each movie
			for i, m in enumerate(movie_data):
				m['id'] = i + 1

			# sort data based on imdbID
			movie_data.sort(key=lambda x: x['id'])

			filtered_data = [movie for movie in movie_data if movie['id'] > movie_id]
			sliced_movies = filtered_data[0:first+1]

			if len(sliced_movies) > first:
				# calculate the client's next cursor.
				last_movie = sliced_movies.pop(-1)
				next_cursor = encode_user_cursor(id=last_movie['id'])
				has_next_page = True
			else:
				# We have reached the last page, and
				# don't have the next cursor.
				next_cursor = None
				has_next_page = False


			# We know that we have items in the
			# previous page window if the initial user ID
			# was not the first one.
			has_previous_page = movie_id > 0

			# build user edges.
			
			edges = [
				Edge(
					node=Movie.from_row(movie),
					cursor=encode_user_cursor(id=movie['id']),
				)
				for movie in sliced_movies
			]


			if edges:
				# we have atleast one edge. Get the cursor
				# of the first edge we have.
				start_cursor = edges[0].cursor
			else:
				# We have no edges to work with.
				start_cursor = None


			if len(edges) > 1:
				# We have atleast 2 edges. Get the cursor
				# of the last edge we have.
				end_cursor = edges[-1].cursor
			else:
				# We don't have enough edges to work with.
				end_cursor = None


			return Connection(
					edges=edges,
					page_info=PageInfo(
						has_next_page=has_next_page,
						has_previous_page=has_previous_page,
						start_cursor=start_cursor,
						end_cursor=end_cursor,
					)
				)

app = FastAPI()

# URL ROUTES
schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)