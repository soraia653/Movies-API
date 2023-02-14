def get_movie_data(s):
  movie_data = requests.get(OMDB_URL.format(s)).json()
  return movie_data

def encode_user_cursor(id: int) -> str:
  return b64encode(f"user:{id}".encode("ascii")).decode("ascii")


def decode_user_cursor(cursor: str) -> int:
  cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
  return int(cursor_data.split(":")[1])