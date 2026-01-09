from html_handles.handle_html_file import load_html_data, create_html_file
from movie_storage.movie_storage_sql import list_movies

WEBSITE_TITLE = "BOGDAN'S MOVIE APP"

def serialize_movie(title, year, poster_img_url):
    """
        Adds for every movie the title, year and poster_img_url
        to an already formatted string for html parsing.
        If one of these fields doesn’t exist, it doesn’t add it.
        Returns the string.
    """
    movie_output = ''
    movie_output += '<li><div class="movie">'
    if poster_img_url != '':
        movie_output += f'<img class="movie-poster" src="{poster_img_url}"/>\n'
    if title != '':
        movie_output += f'<div class="movie-title">{title}</div>\n'
    if year != '':
        movie_output += f'<div class="movie-year">{year}</div>\n'
    movie_output += '</div></li>\n'

    return movie_output


def format_movies_html():
    """
        Gets the movies from the database,
        then calls the function that adds information of every
        movie into a string formatted like html.
        Returns this string.
    """
    output = ''
    movies = list_movies()
    for title, data in movies.items():
            output += serialize_movie(title, data['year'], data['poster_img_url'])
    return output


def generate_website():
    """
        Loads the html template and movies information into string data.
        Replaces the template text from the "index_template.html" with
        movies information.
        Then calls the function to generate the new html file with movies information.
    """
    html_template = load_html_data("templates/index_template.html")
    movies_information = format_movies_html()
    new_html_content = html_template.replace('__TEMPLATE_TITLE__', WEBSITE_TITLE)
    new_html_content = new_html_content.replace('__TEMPLATE_MOVIE_GRID__', movies_information)
    create_html_file(new_html_content)
    print("Website was generated successfully.")
