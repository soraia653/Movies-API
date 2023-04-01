from base64 import b64encode, b64decode
import requests

from settings import OMDB_API_KEY, OMDB_URL
from schema import Movie, MovieResult, PageInfo


def encode_movie_cursor(movie_id: int) -> str:
    """Encode the given movie ID into a cursor."""
    return b64encode(f"movie:{movie_id}".encode("ascii")).decode("ascii")


def decode_movie_cursor(cursor: str) -> int:
    """Decodes the given movie ID from a cursor."""
    movie_cursor = b64decode(cursor.encode("ascii")).decode("ascii")
    return int(movie_cursor.split(":")[1])


def get_movies(query: str, limit: int = None, cursor: str = None) -> MovieResult:
    """
    Requests all movies related to specific movie search.
    """
    movies = []
    total_results = 0
    movie_id = 0
    page = 1

    params = {"apikey": OMDB_API_KEY, "s": query, "page": page}

    if cursor is not None:
        mov_id = decode_movie_cursor(cursor=cursor)
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

    filtered_movies = list(filter(lambda movie: movie.id >= mov_id, movies))

    sliced_movies = filtered_movies[: limit + 1]

    if len(sliced_movies) > limit:
        last_movie = sliced_movies.pop(-1)
        next_cursor = encode_movie_cursor(movie_id=last_movie.id)
    else:
        next_cursor = None

    return MovieResult(
        total_results=total_results,
        movies=sliced_movies,
        page_info=PageInfo(next_cursor=next_cursor),
    )
