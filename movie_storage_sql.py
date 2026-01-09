from sqlalchemy import create_engine, text

# Define the database URL and database engine
DB_URL = "sqlite:///movies.db"
DATA_ENGINE = create_engine(DB_URL, echo=False)


def set_up_database():
    """
    Creates the database engine and the movies table if it doesn't exist.
    """

    with DATA_ENGINE.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_img_url TEXT
            )
        """))
        connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with DATA_ENGINE.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster_img_url FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster_img_url": row[3]} for row in movies}


def add_movie_to_storage(title, year, rating, poster_img_url):
    """Add a new movie to the database."""
    with DATA_ENGINE.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_img_url) VALUES (:title, :year, :rating, :poster_img_url)"),
                               {"title": title, "year": year, "rating": rating, "poster_img_url": poster_img_url})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as error:
            print(f"Error: {error}")


def delete_movie_from_storage(title):
    """Delete a movie from the database."""
    with DATA_ENGINE.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE lower(title) = :title"),
                               {"title": title.lower()})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as error:
            print(f"Error: {error}")


def update_movie_from_storage(title, rating):
    """Update a movie's rating in the database."""
    with DATA_ENGINE.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as error:
            print(f"Error: {error}")


def is_movie_in_storage(title):
    """ Finds if a movie is in database """
    movies = list_movies()
    for movie in movies.keys():
        if movie.lower() == title.lower():
            return True
    return False