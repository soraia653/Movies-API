import requests
from settings import OMDB_API_KEY
from schema import Movie, MovieResult


def get_movies(query: str, page: int = 1) -> MovieResult:
    """
    Requests all movies related to specific movie search.
    Outputs to MovieResult class.
    """
    movies = []
    total_results = 0
    movie_id = 0

    params = {"apikey": OMDB_API_KEY, "s": query, "page": page}

    while True:
        try:
            response = requests.get("http://www.omdbapi.com/", params=params, timeout=1)
        except requests.exceptions.Timeout:
            print("Timeout raised, recovering.")

        movie_data = response.json()

        if movie_data["Response"] == "True":
            total_results = int(movie_data["totalResults"])

            for m in movie_data["Search"]:
                movie_id += 1
                movies += [
                    Movie(
                        Title=m["Title"],
                        Year=m["Year"],
                        imdbID=m["imdbID"],
                        Type=m["Type"],
                        Poster=m["Poster"],
                        id=movie_id,
                    )
                ]

            if len(movies) >= total_results:
                break
            page += 1
            params["page"] = page
        else:
            return None
    return MovieResult(total_results=total_results, movies=movies)
