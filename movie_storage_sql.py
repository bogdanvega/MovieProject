from sqlalchemy import create_engine, text

# Define the database URL and database engine
DB_URL = "sqlite:///movies.db"
DATA_ENGINE = create_engine(DB_URL, echo=True)

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
                rating REAL NOT NULL
            )
        """))
        connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with DATA_ENGINE.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with DATA_ENGINE.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"),
                               {"title": title, "year": year, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as error:
            print(f"Error: {error}")


def delete_movie(title):
    """Delete a movie from the database."""
    pass


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    pass
