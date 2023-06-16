import sys

from requests.exceptions import HTTPError
from pathlib import Path
from dotenv import load_dotenv
import requests
from book import Book
import os

"""
@author MfellnerDev | Manuel Fellner
@version 16.06.2023
"""

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

# Options: "markdown", "pdf", "plaintext"
EXPORT_TYPE = os.getenv('EXPORT_TYPE')

# Get the name & extension of the file where all info will be stored
INFO_FILE = os.getenv('INFO_FILE')

# Open a new session and set the correct authentication headers
session = requests.Session()
session.headers.update(AUTH_HEADER)


def _remove_substring_out_of_string(string: str, substring: str):
    """
    Just remove an unwanted substring out of a string, in our case the "\n" substring
    :param string:
    :param substring:
    :return: string without substring
    """
    return string.replace(substring, '')


def _get_export_file_extension():
    """
    Return the suiting file extension for the selected export type
    :return: md, pdf or txt
    """
    if EXPORT_TYPE == 'markdown':
        return 'md'
    elif EXPORT_TYPE == 'pdf':
        return 'pdf'
    elif EXPORT_TYPE == 'plaintext':
        return 'txt'


def _create_necessary_folders_windows(parent_book_slug_slug):
    """
    Creates the needed folders for exporting all pages on Windows OS
    :param parent_book_slug_slug:
    :return:
    """
    current_directory = os.getcwd()

    if not os.path.exists(f'{current_directory}\\exports\\{EXPORT_TYPE}'):
        os.makedirs(f'{current_directory}\\exports\\{EXPORT_TYPE}')

    if not os.path.exists(f'{current_directory}\\exports\\{EXPORT_TYPE}\\{parent_book_slug_slug}'):
        os.makedirs(f'{current_directory}\\exports\\{EXPORT_TYPE}\\{parent_book_slug_slug}')


def _create_necessary_folders_linux(parent_book_slug_slug):
    """
    Creates the needed folders for exporting all pages on Linux OS
    :param parent_book_slug_slug:
    :return:
    """
    current_directory = os.getcwd()

    if not os.path.exists(f'{current_directory}/exports/{EXPORT_TYPE}'):
        os.makedirs(f'{current_directory}/exports/{EXPORT_TYPE}')

    if not os.path.exists(f'{current_directory}/exports/{EXPORT_TYPE}/{parent_book_slug_slug}'):
        os.makedirs(f'{current_directory}/exports/{EXPORT_TYPE}/{parent_book_slug_slug}')


def _build_correct_export_path(parent_book_slug_slug, page_id, page_slug):
    """
    Create the correct folders for the export and build the correct filename for an individual page
    :return:
    """

    current_directory = os.getcwd()

    # Check which OS the host is running -> for creating the correct folders
    if sys.platform.startswith('win'):
        _create_necessary_folders_windows(parent_book_slug_slug)
    elif sys.platform.startswith('linux'):
        _create_necessary_folders_linux(parent_book_slug_slug)

    # Build the complete export path with the current directory and exports/export_type
    export_directory_path = os.path.join(current_directory, 'exports', EXPORT_TYPE)

    # Get the current file extension from the EXPORT_TYPE variable
    file_extension = _get_export_file_extension()
    # build the file_name with [page_slug].[file_extension]
    file_name = f'{page_slug}.{file_extension}'
    # Return the path of the individual page, formatted in: [current_directory]/[parent_book_slug_slug]/[filename]
    return os.path.join(export_directory_path, parent_book_slug_slug, file_name)


def _read_file_and_store_info_in_list():
    """
    Read the INFO_FILE, convert all information into Book objects and put these objects into an object-list.
    Easy attribute-handling, hehe
    :return:
    """
    book_list = []
    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        # go through all lines
        for current_line in info_file:
            # Split the information, format: [page_id]:[page_slug]:[parent_book_slug_slug]
            page_info = current_line.split(':')
            # Store the id
            page_id = page_info[0]
            # Store the slug but remove the "\n" sign
            page_slug = _remove_substring_out_of_string(page_info[1], '\n')
            # Store the slug of the parent book of the entry
            parent_book_slug = _remove_substring_out_of_string(page_info[2], '\n')

            # build the path, where the page should be stored - filename
            filename = _build_correct_export_path(parent_book_slug, page_id, page_slug)

            # store the values in the object list
            book_list.append(Book(parent_book_slug, page_id, page_slug, filename))
    return book_list


def _export_and_store_pages():
    """
    Export all the pages via BookStack API /api/pages/{page_id}/export/{filetype}
    :return:
    """
    book_list = _read_file_and_store_info_in_list()

    for book in book_list:
        try:
            # try to download the exported page file in the expected format
            exported_page = session.get(f'{BOOKSTACK_URL}/api/pages/{book.page_id}/export/{EXPORT_TYPE}')
            filename_object = Path(book.filename)
            # write the page.content (so bytecode) in the real file
            filename_object.write_bytes(exported_page.content)

            print(f'Successfully exported & stored file "{book.filename}".')
        except HTTPError as http_err:
            print(f'Oh, no! An HTTP Error occurred! Error: {http_err}')
        except Exception as err:
            print(f'Oh, no! An Error occurred! Error: {err}')


_export_and_store_pages()
