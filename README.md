# Simple API using Python and Strawberry

Implemented a simple API that fetches movie data using the OMDB API.

## Requirements

Python 3.9 or higher
Docker and Docker Compose (optional)

## Configuration

You can configure the API by modifying the settings in the app/settings.py file.

## Getting Started

To get started, follow these instructions:

1. Clone this repository

```bash
git clone https://github.com/soraia653/movies-api.git
cd movies-api
```

2. Install required dependencies:

```bash
poetry install
```

3. Run the API:

```bash
python app/main.py
```

This will start the API and make it available at http://localhost:8000/graphql.

You can use a GraphQL client like GraphiQL or GraphQL Playground to interact with the API.

## Running with Docker Compose

Alternatively, you can run the API using Docker Compose:

1. Clone this repository

```bash
git clone https://github.com/soraia653/movies-api.git
cd movies-api
```

2. Build and start the Docker container:

```bash
docker-compose up -d
```

## Testing

To run the tests, use the following command:

```bash
pytest
```

This will run all the tests in the tests directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Usage/Examples

Query

```bash
query getMovies {
  getMovie(title: "Harry Potter", first: 2) {
    edges {
      node {
        id
        imdbID
        Title
        Type
        Poster
      }
    }
    pageInfo {
      hasNextPage
    }
  }
}
```

Expected Result

```
{
  "data": {
    "getMovie": {
      "edges": [
        {
          "node": {
            "id": 1,
            "imdbID": "tt1201607",
            "Title": "Harry Potter and the Deathly Hallows: Part 2",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BMGVmMWNiMDktYjQ0Mi00MWIxLTk0N2UtN2ZlYTdkN2IzNDNlXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg"
          }
        },
        {
          "node": {
            "id": 2,
            "imdbID": "tt0241527",
            "Title": "Harry Potter and the Sorcerer's Stone",
            "Type": "movie",
            "Poster": "https://m.media-amazon.com/images/M/MV5BNmQ0ODBhMjUtNDRhOC00MGQzLTk5MTAtZDliODg5NmU5MjZhXkEyXkFqcGdeQXVyNDUyOTg3Njg@._V1_SX300.jpg"
          }
        }
      ],
      "pageInfo": {
        "hasNextPage": true
      }
    }
  }
}
```

## Lessons Learned

I decided to use Strawberry instead of Graphene since it is the recommended library as per FastAPI documentation.

While working on this project, one of the steps was applying Pagination to the query. I quickly realized that Strawberry's documentation had many errors and their tutorial did not work. I spent some time on this issue and was able to fix.

I ended up opening a PR request w/ Strawberry to fix their documentation.

- [Cursor Pagination does not work](https://github.com/strawberry-graphql/strawberry/pull/2554) # 2544

The moral of the story is that with one simple project I ended up contributing to an open-source project (albeit a very small contribution) and perhaps helping someone use this library.
