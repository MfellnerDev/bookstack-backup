import requests
from requests.exceptions import HTTPError
import os
from dotenv import load_dotenv
import random

# Load all environment vars from .env
load_dotenv()

# URL to your BookStack instance
BOOKSTACK_URL = os.getenv('BOOKSTACK_URL')

print(f"The URL of your BookStack instance is \"{BOOKSTACK_URL}\". ")

# Token information of Admin user
TOKEN_ID = os.getenv('TOKEN_ID')
TOKEN_SECRET = os.getenv('TOKEN_SECRET')

# The auth header -> see BookStack API documentation
AUTH_HEADER = {'Authorization': f'Token {TOKEN_ID}:{TOKEN_SECRET}'}

# Get the name & extension of the file where all info will be stored
INFO_FILE = os.getenv('INFO_FILE')

# Open a new session and set the correct authentication headers
session = requests.Session()
session.headers.update(AUTH_HEADER)


def _get_page_list_json():
    """
    Fetch the information of all BookStack pages. Includes ID, slug, name, etc.
    :return: fetched information as parsed JSON
    """

    print("Trying to get a list of all BookStack pages...")

    try:
        # send a request to the /pages/ api endpoints -> returns json with all pages and infos
        get_page_list = session.get(f"{BOOKSTACK_URL}/api/pages")

        # raise error if one occurs
        get_page_list.raise_for_status()

        # return the page list as parsed json
        return get_page_list.json()

    except HTTPError as http_err:
        print(f'Oh, no! An HTTP Error occurred! Error: {http_err}')
    except Exception as err:
        print(f'Oh, no! An Error occurred! Error: {err}')


def _append_str_to_file(filename: str, content: str):
    """
    Checks if the file exists and if it does, APPEND the content to it
    :param filename: name of file
    :param content: content that should get appended
    :return:
    """
    if os.path.exists(filename):
        with open(filename, 'a', encoding='utf-8') as file:
            file.writelines(f"{content}\n")


def _create_new_file(filename: str):
    """
    Create a new file with a specific filename, don't forget the extension!
    :param filename: name of file
    :return:
    """
    open(f'{filename}', 'w', encoding='utf-8').close()


def _check_slug(slug: str):
    """
    Validate the slug - Check if the slug is empty and if so, give it a value in the format:
    "empty-slug-[RANDOM_NUMBER_FROM_1_TO_1000]"
    :param slug: the slug
    :return: if slug empty, a new slug. If not empty, the current slug
    """
    if not slug:
        return f'empty-slug-{random.randint(1, 1000)}'
    return slug


def _get_and_store_all_page_infos_in_file():
    # Get the pages information from the API (as json but can be treated like dictionary)
    page_dict = _get_page_list_json()

    if page_dict is None:
        raise ValueError("The page information is None!")

    print("All pages were fetched from the API!")

    # Get the total amount of pages and inform the user
    print(f"A total amount of {page_dict.pop('total', {})} will be added to the file.")

    _create_new_file(INFO_FILE)

    for element_list in page_dict.values():
        for specific_element in element_list:
            page_id = str(specific_element['id'])
            page_slug = _check_slug(str(specific_element['slug']))
            # store ID and SLUG of the page in the format "id:slug"\n in the INFO textfile
            content = f"{page_id}:{page_slug}"
            _append_str_to_file(INFO_FILE, content)


_get_and_store_all_page_infos_in_file()
