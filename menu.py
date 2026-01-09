import handle_movies
from movies_web_generator import generate_website

def print_main_menu():
    """ Function that displays the main menu. """
    print()
    print("Menu:")
    print("0: Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Generate website")
    print()


def get_user_choice():
    """ Function that returns the user choice. """
    return input("Enter choice (0-9): ")


def exit_app():
    """ Function that exits the app."""
    print("Bye!")

def back_to_main_menu():
    """
    Defining the function that gets the user back to the main menu of the movie database.
    """
    print()
    input("Press enter to continue")

def doing_what_the_user_wants():
    """ Defining the function that calls all the other functions
    depending on the user input.
    """
    while True:
        print_main_menu()
        user_choice = get_user_choice()

        if user_choice == "0":
            exit_app()
            break

        if user_choice not in dispatch_table:
            print("Invalid choice")
            back_to_main_menu()
            continue

        dispatch_table[user_choice]()
        back_to_main_menu()


dispatch_table = {
    "1": handle_movies.print_all_movies,
    "2": handle_movies.add_movie,
    "3": handle_movies.delete_movie,
    "4": handle_movies.update_movie,
    "5": handle_movies.print_movie_database_stats,
    "6": handle_movies.print_random_movie,
    "7": handle_movies.print_searched_movie,
    "8": handle_movies.print_movies_sorted_by_rating,
    "9": generate_website
}
