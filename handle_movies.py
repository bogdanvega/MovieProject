import os
from dotenv import load_dotenv
import random
import requests
from statistics import mean, median, StatisticsError
import movie_storage_sql as storage

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_URL = f"http://www.omdbapi.com/?apikey={API_KEY}&"

def print_all_movies():
    """ Retrieve and display all movies from the database. """
    movies = storage.list_movies()
    print(f"\n{len(movies)} movie(s) in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def is_movie_rating_valid(movie_rating):
    """ Function that validates the movie rating """
    if movie_rating.isdigit() and 0 <= int(movie_rating) <= 10:
        return True
    if "." in movie_rating:
        split_rating = movie_rating.split(".")
        if split_rating[0].isdigit() and split_rating[1].isdigit():
            if float(movie_rating) < 0 or float(movie_rating) > 10:
                return False
            return True
        return False
    return False


def is_movie_year_valid(movie_year):
    """ Function that validates if the movie year is valid """
    return movie_year.isdigit() and int(movie_year) >= 1888


def get_movie_name():
    """ Function that gets the movie name from the user.
    Validates the input as well.
    """
    movie_name = input("\nEnter new movie name: ")
    if storage.is_movie_in_storage(movie_name):
        print(f"Movie {movie_name} is already in your database!")
        return 0
    if movie_name.isspace() or movie_name == "":
        print("Movie name must not be empty.")
        return 0
    return movie_name


def get_movie_year():
    """ Function that gets the movie year from the user.
    Validates the input as well.
    """
    while True:
        movie_year = input("Enter new movie year: ")
        if not is_movie_year_valid(movie_year):
            print(f"Year {movie_year} is invalid.")
            continue
        return movie_year


def get_movie_rating():
    """ Function that gets the movie rating from the user.
    Validates the input as well.
    """
    while True:
        movie_rating = input("Enter new movie rating (0-10): ")
        try:
            if is_movie_rating_valid(movie_rating):
                return movie_rating
            print(f"Rating {movie_rating} is invalid.")
            continue
        except ValueError as error:
            print(f"Rating {movie_rating} is invalid. Reason: {error}")


def add_movie():
    """
    Function that gets the title of the movie from the user.
    Then fetches the movie data from the API and
    adds the movie into the database.
    """
    try:
        new_movie_name = get_movie_name()
        if new_movie_name == 0: # case of movie already added or movie name empty
            pass
        else:
            request_url = API_URL + f"t={new_movie_name}"
            response = requests.get(request_url)
            if response.status_code != requests.codes.ok:
                print(f"Error: {response.status_code}, {response.text}")
            else:
                movie_data = response.json()
                if movie_data == {"Response": "False","Error": "Movie not found!"}:
                    print(f"The movie {new_movie_name} doesn't exist.")
                else:
                    title = movie_data.get("Title")
                    year = movie_data.get("Year")
                    rating = movie_data.get("imdbRating")
                    poster_img_url = movie_data.get("Poster")
                    storage.add_movie_to_storage(title, year, rating, poster_img_url)
    except requests.exceptions.ConnectionError:
        print("The internet connection is not working. Try again!")


def delete_movie():
    """ Function that gets the name of the movie from the user.
    Then calls the function that deletes the movie from the database.
    """
    movie_title_to_delete = input("\nEnter movie name to delete: ")
    if not storage.is_movie_in_storage(movie_title_to_delete):
        print(f"Movie {movie_title_to_delete} doesn't exist!")
    else:
        storage.delete_movie_from_storage(movie_title_to_delete)


def update_movie():
    """ Function that gets from the user the name and the
    rating of a movie. Function checks if the rating is a valid one
    and calls the function that updates the movie in the database.
    """

    print()
    movie_name_to_update = input("Enter movie name: ")
    while True:
        if not storage.is_movie_in_storage(movie_name_to_update):
            print(f"Movie {movie_name_to_update} doesn't exist!")
            break
        new_movie_rating = input("Enter new movie rating (0-10): ")
        try:
            if not is_movie_rating_valid(new_movie_rating):
                print("Please enter a valid rating")
                continue
            rating = float(new_movie_rating)
            storage.update_movie_from_storage(movie_name_to_update, rating)
            print(f"Movie {movie_name_to_update} successfully updated")
            break
        except ValueError:
            print("Please enter a valid rating")

def get_average_rating():
    """ Function that returns the average rating of the list of movies."""
    movies = storage.list_movies()

    try:
        return mean(data['rating'] for movie, data in movies.items())
    except StatisticsError:
        return "0 : There are no movies in the database."


def get_median_rating():
    """ Function that returns the median rating of the list of movies. """
    movies = storage.list_movies()

    try:
        return median([data["rating"] for data in movies.values()])
    except StatisticsError:
        return "0 : There are no movies in the database."


def get_best_movies():
    """
    Returning the best movie/movies.
    The movies are sorted by rating, the best being the first one.
    Max rating is initialized with the rating of the first movie.
    Then we are looping through the movies, and we add all the movies
    with the max rating to a list. When a movie that has a rating
    lower than the max rating is reached, we exit the loop.
    """
    movies = storage.list_movies()

    movies_sorted = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
    max_rating = movies_sorted[0][1]['rating']
    list_of_best_movies = []
    for movie, data in movies_sorted:
        if data['rating'] == max_rating:
            list_of_best_movies.append((movie, data))
        else:
            break
    return list_of_best_movies


def get_worst_movies():
    """
    Returning the worst movie/movies.
    The movies are sorted by rating, the worst being the first one.
    Min rating is initialized with the rating of the first movie.
    Then we are looping through the movies, and we add all the movies
    with the min rating to a list. When a movie that has a rating
    higher than the min rating is reached, we exit the loop.
    """
    movies = storage.list_movies()

    movies_sorted = sorted(movies.items(), key=lambda item: item[1]['rating'])
    min_rating = movies_sorted[0][1]['rating']
    list_of_worst_movies = []
    for movie, data in movies_sorted:
        if data['rating'] == min_rating:
            list_of_worst_movies.append((movie, data))
        else:
            break
    return list_of_worst_movies


def print_movie_database_stats():
    """ Function that displays the stats from the list of movies :
    Average rating, Median rating, Best movie(s) and Worst movie(s). """

    print()
    print("Average rating: ", get_average_rating())
    print("Median rating: ", get_median_rating())

    label_best_movies = "Best movie(s): "
    print(label_best_movies, end="")
    for i, (movie, data) in enumerate(get_best_movies()):
        if i == 0:
            print(f"{movie} ({data['year']}): {data['rating']}")
        else:
            print(" " * len(label_best_movies)
                  + f"{movie} ({data['year']}): {data['rating']}")

    label_worst_movies = "Worst movie(s): "
    print(label_worst_movies, end="")
    for i, (movie, data) in enumerate(get_worst_movies()):
        if i == 0:
            print(f"{movie} ({data['year']}): {data['rating']}")
        else:
            print(" " * len(label_worst_movies)
                  + f"{movie} ({data['year']}): {data['rating']}")

def print_random_movie():
    """ Function that displays a randomly selected movie """
    movies = list(storage.list_movies().items())

    title, data = random.choice(movies)
    print(f"Your movie for tonight: {title} "
          f"({data['year']}), it's rated {data['rating']}")


def print_searched_movie():
    """ Function that displays the movies that matches the part of
    a movie title provided by the user. """
    movies = storage.list_movies()

    part_of_movie_name = input("\nEnter part of movie name: ")
    for title, data in movies.items():
        if part_of_movie_name.lower() in title.lower():
            print(f"{title} ({data['year']}), {data['rating']}")


def print_movies_sorted_by_rating():
    """ Function that displays the database movies sorted by rating. """
    movies = storage.list_movies()

    print()
    movies_sorted = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
    for title, data in movies_sorted:
        print(f"{title} ({data['year']}): {data['rating']}")
