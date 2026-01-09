import json

def get_movies():
    """
        Returns a list of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.
        """
    with open("../data/movies.json", "r") as file_obj:
        movies = json.loads(file_obj.read())
    return movies


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open("../data/movies.json", "w") as file_obj:
        file_obj.write(json.dumps(movies))

def add_movie_to_storage(title, year, rating):
    """
    Function that adds a new movie to the movie database.
    """
    movies = get_movies()

    new_movie = {'name': title,
                 'year': year,
                 'rating': float(rating)}
    movies.append(new_movie)

    save_movies(movies)

def delete_movie_from_storage(title):
    """ Function that deletes a movie from the movie database.
    Using a for loop to find the movie. When movie is found, we are
    deleting it, and we are exiting the for loop to be efficient.
    """
    movies = get_movies()

    for movie in movies:
        if movie['name'] == title:
            movies.remove(movie)
            break

    save_movies(movies)


def update_movie_from_storage(title, rating):
    """ Function that updates a desired movie with a new rating.
    Using a for loop to find the movie. When movie is found, the
    rating is updated, and we are exiting the for loop to be efficient.
    """
    movies = get_movies()

    for movie in movies:
        if movie["name"] == title:
            movie["rating"] = rating
            break

    save_movies(movies)

def is_movie_in_storage(title):
    """ Finds if a movie is in database """
    movies = get_movies()
    for movie in movies:
        if movie["name"] == title:
            return True
    return False
