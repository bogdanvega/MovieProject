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