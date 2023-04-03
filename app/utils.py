from base64 import b64decode, b64encode

import requests

from app.schema import Movie, MovieConnection, MovieEdge, PageInfo
from app.settings import OMDB_API_KEY, OMDB_URL


def encode_movie_cursor(movie_id: int) -> str:
    """Encode the given movie ID into a cursor."""
    return b64encode(f"movie:{movie_id}".encode("ascii")).decode("ascii")


def decode_movie_cursor(cursor: str) -> int:
    """Decodes the given movie ID from a cursor."""
    movie_cursor = b64decode(cursor.encode("ascii")).decode("ascii")
    return int(movie_cursor.split(":")[1])


def get_movies(query: str, first: int, after: str) -> MovieConnection:
    """
    Requests all movies related to specific movie search.
    """
    movies = []
    total_results = 0
    movie_id = 0
    page = 1

    params = {"apikey": OMDB_API_KEY, "s": query, "page": page}

    if after is not None:
        mov_id = decode_movie_cursor(cursor=after)
    else:
        mov_id = 0

    # get all results from search
    while True:
        try:
            response = requests.get(OMDB_URL, params=params, timeout=1)
        except requests.exceptions.Timeout:
            print("Timeout raised, recovering.")

        # data in dict format
        movie_data = response.json()

        if movie_data["Response"] == "True":
            total_results = int(movie_data["totalResults"])

            for movie in movie_data["Search"]:
                movie_id += 1

                movies += [Movie.from_row(movie, movie_id)]

            if len(movies) >= total_results:
                break
            page += 1
            params["page"] = page
        else:
            return None

    filtered_movies = list(filter(lambda movie: movie.id > mov_id, movies))

    sliced_movies = filtered_movies[0:first]

    has_next_page = len(filtered_movies) > max(len(sliced_movies), first)

    has_previous_page = mov_id > 0

    edges = [
        MovieEdge(
            node=mov_object, cursor=encode_movie_cursor(movie_id=mov_object.id)
        )
        for mov_object in sliced_movies
    ]

    if edges:
        start_cursor = edges[0].cursor
    else:
        start_cursor = None

    if len(edges) > 1:
        end_cursor = edges[-1].cursor
    else:
        end_cursor = None

    return MovieConnection(
        total_results=total_results,
        movies=edges,
        page_info=PageInfo(
            has_next_page=has_next_page,
            has_previous_page=has_previous_page,
            start_cursor=start_cursor,
            end_cursor=end_cursor,
        ),
    )
