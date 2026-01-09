

def load_html_data(html_file_path):
    """ Loads a html file """
    with open(html_file_path, 'r') as file_object:
        return file_object.read()


def create_html_file(html_data):
    """ Creates a new html file with the given data """
    with open('index.html', 'w') as file_object:
        return file_object.write(html_data)