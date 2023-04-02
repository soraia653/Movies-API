from app.utils import encode_movie_cursor, decode_movie_cursor, get_movies


class TestUtils:
    """Test all functions within utils.py file."""

    def test_encode_movie_cursor(self):
        """Test encode function."""
        cursor = encode_movie_cursor(123)
        assert cursor == "bW92aWU6MTIz"

    def test_decode_movie_cursor(self):
        """Test decode_movie_cursor() function."""
        cursor = decode_movie_cursor("bW92aWU6MTIz")
        assert cursor == 123

    def test_get_movies_no_results(self):
        """Test that the function returns None if there are no results."""
        movies = get_movies(query="invalid query", first=10, after=None)
        assert movies is None

    def test_get_movies(self):
        movies = get_movies(query="Harry Potter", first=3, after=None)
        assert movies is not None
        assert movies.total_results > 0
        assert len(movies.movies) == 3
        assert movies.page_info.has_previous_page is False
        assert movies.page_info.has_next_page is True
        assert movies.page_info.start_cursor is not None
        assert movies.page_info.end_cursor is not None
