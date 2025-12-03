import random
from statistics import mean, median, StatisticsError
import movie_storage
from movie_storage import get_movies


def print_all_movies():
    """ Displaying the total number of movies and every movie in the database """
    movies = get_movies()
    print(f"\n{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie['name']} ({movie['year']}): {movie['rating']}")


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
    while True:
        movie_name = input("\nEnter new movie name: ")
        if movie_storage.is_movie_in_storage(movie_name):
            print(f"Movie {movie_name} already exists!")
            continue
        if movie_name.isspace() or movie_name == "":
            print("Movie name must not be empty.")
            continue
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
    Function that gets the name, year and rating from the user.
    Calls the function that saves the movie in the database.
    """
    new_movie_name = get_movie_name()
    new_movie_year = get_movie_year()
    new_movie_rating = get_movie_rating()

    movie_storage.add_movie_to_storage(new_movie_name, new_movie_year, new_movie_rating)
    print(f"Movie {new_movie_name} successfully added")

def delete_movie():
    """ Function that gets the name of the movie from the user.
    Then calls the function that deletes the movie from the database.
    """
    while True:
        movie_name_to_delete = input("\nEnter movie name to delete: ")
        if not movie_storage.is_movie_in_storage(movie_name_to_delete):
            print(f"Movie {movie_name_to_delete} doesn't exist!")
            break
        movie_storage.delete_movie_from_storage(movie_name_to_delete)
        print(f"Movie {movie_name_to_delete} successfully deleted")
        break


def update_movie():
    """ Function that gets from the user the name and the
    rating of a movie. Function checks if the rating is a valid one
    and calls the function that updates the movie in the database.
    """

    print()
    movie_name_to_update = input("Enter movie name: ")
    while True:
        if not movie_storage.is_movie_in_storage(movie_name_to_update):
            print(f"Movie {movie_name_to_update} doesn't exist!")
            break
        new_movie_rating = input("Enter new movie rating (0-10): ")
        try:
            if not is_movie_rating_valid(new_movie_rating):
                print("Please enter a valid rating")
                continue
            rating = float(new_movie_rating)
            movie_storage.update_movie_from_storage(movie_name_to_update, rating)
            print(f"Movie {movie_name_to_update} successfully updated")
            break
        except ValueError:
            print("Please enter a valid rating")

def get_average_rating():
    """ Function that returns the average rating of the list of movies."""
    movies = get_movies()

    try:
        return mean(movie['rating'] for movie in movies)
    except StatisticsError:
        return "0 : There are no movies in the database."


def get_median_rating():
    """ Function that returns the median rating of the list of movies. """
    movies = get_movies()

    movies_sorted = sorted(movies, key=lambda movie: movie['rating'])
    try:
        return median(movie['rating'] for movie in movies_sorted)
    except StatisticsError:
        return "0 : There are no movies in the database."


def get_best_movies():
    """ Returning the best movie/movies.
    First, the list is sorted by rating, the best being the first one.
    Max rating is initialized with the rating of the first movie.
    Then we are looping through the movies, and we add all the movies
    with the max rating to a list. When a movie that has a rating
    lower than the max rating is reached, we exit the loop.
    """
    movies = get_movies()

    movies_sorted = sorted(movies, key=lambda m: m['rating'], reverse=True)
    max_rating = movies_sorted[0]['rating']

    list_of_best_movies = []
    for movie in movies_sorted:
        if movie['rating'] == max_rating:
            list_of_best_movies.append(movie)
        else:
            break
    return list_of_best_movies


def get_worst_movies():
    """
    Returning the worst movie/movies.
    First, the list is sorted by rating, the worst being the first one.
    Min rating is initialized with the rating of the first movie.
    Then we are looping through the movies, and we add all the movies
    with the min rating to a list. When a movie that has a rating
    higher than the min rating is reached, we exit the loop.
    """
    movies = get_movies()

    movies_sorted = sorted(movies, key=lambda m: m['rating'])
    min_rating = movies_sorted[0]['rating']

    list_of_worst_movies = []
    for movie in movies_sorted:
        if movie['rating'] == min_rating:
            list_of_worst_movies.append(movie)
        else:
            break
    return list_of_worst_movies


def print_movie_database_stats():
    """ Function that displays the list of movies stats:
    Average rating, Median rating, Best movie(s) and Worst movie(s). """

    print()
    print("Average rating: ", get_average_rating())
    print("Median rating: ", get_median_rating())

    label_best_movies = "Best movie(s): "
    print(label_best_movies, end="")
    for i, movie in enumerate(get_best_movies()):
        if i == 0:
            print(f"{movie['name']} ({movie['year']}): {movie['rating']}")
        else:
            print(" " * len(label_best_movies)
                  + f"{movie['name']} ({movie['year']}): {movie['rating']}")

    label_worst_movies = "Worst movie(s): "
    print(label_worst_movies, end="")
    for i, movie in enumerate(get_worst_movies()):
        if i == 0:
            print(f"{movie['name']} ({movie['year']}): {movie['rating']}")
        else:
            print(" " * len(label_worst_movies)
                  + f"{movie['name']} ({movie['year']}): {movie['rating']}")


def print_random_movie():
    """ Function that displays a randomly selected movie """
    movies = get_movies()

    movie_choice = random.choice(movies)
    print(f"Your movie for tonight: {movie_choice['name']} "
          f"({movie_choice['year']}), it's rated {movie_choice['rating']}")


def print_searched_movie():
    """ Function that displays the movies that matches the part of
    a movie title provided by the user. """
    movies = get_movies()

    part_of_movie_name = input("\nEnter part of movie name: ")
    for movie in movies:
        if part_of_movie_name.lower() in movie['name'].lower():
            print(f"{movie['name']} ({movie['year']}), {movie['rating']}")


def print_movies_sorted_by_rating():
    """ Function that displays the database movies sorted by rating. """
    movies = get_movies()

    print()
    movies_sorted = sorted(movies, key=lambda m: m['rating'], reverse=True)
    for movie in movies_sorted:
        print(f"{movie['name']} "
              f"({movie['year']}): {movie['rating']}")
