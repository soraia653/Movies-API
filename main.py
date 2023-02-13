from fastapi import FastAPI
import requests
import graphene

OMDB_URL = "http://www.omdbapi.com/?apikey=c05820ad&t={}"

app = FastAPI()


def get_movie_data(t):
  movie_data = requests.get(OMDB_URL.format(t)).json()
  return movie_data


@app.get("/")
async def index():
  return {"message": "Greetings!"}


@app.get("/movie/{movie_name}")
async def get_movie(movie_name):
  movie = get_movie_data(movie_name)
  return movie