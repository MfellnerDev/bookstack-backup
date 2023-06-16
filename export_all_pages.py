import requests
from requests.exceptions import HTTPError
from pathlib import Path
import os
from dotenv import load_dotenv

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

element_dict = {}


def _remove_substring_out_of_string(string: str, substring: str):
    """
    Just remove an unwanted substring out of a string, in our case the "\n" substring
    :param string:
    :param substring:
    :return: string without substring
    """
    return string.replace(substring, '')


def _read_file_and_store_info_in_dict():
    """
    Read the INFO_FILE and store it in a dictionary
    -> see INFO_FILE environment variable
    :return:
    """
    page_info_dict = {}
    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        # go through all lines
        for current_line in info_file:
            # Split the information, format: [page_id]:[page_slug]
            page_info = current_line.split(':')
            # Store the id
            page_id = page_info[0]
            # Store the slug but remove the "\n" sign
            page_slug = _remove_substring_out_of_string(page_info[1], '\n')
            # store the values in the dictionary
            page_info_dict[page_id] = page_slug
    return page_info_dict


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


def _build_correct_export_path():
    """
    Build the correct path/Filename from the given information.
    export files are ALWAYS stored in [current_directory]/exports/[export_type]
    :return:
    """

    current_directory = os.getcwd()

    # if the /exports folder doesn't exist -> create it
    if not os.path.exists(f'{current_directory}\exports\{EXPORT_TYPE}'):
        os.makedirs(f'{current_directory}\exports\{EXPORT_TYPE}')

    # Build the complete export path with the current directory and exports/export_type
    export_directory_path = os.path.join(current_directory, 'exports', EXPORT_TYPE)
    print(f'All the exported {EXPORT_TYPE}-files will be stored in "{export_directory_path}".')

    # get the entire page info and store it in dictionary
    page_info_dict = _read_file_and_store_info_in_dict()

    full_filename_list = []
    file_extension = _get_export_file_extension()

    if page_info_dict:
        for page_id in page_info_dict.keys():
            # build the file_name with [page_slug].[file_extension]
            file_name = f'{page_info_dict[page_id]}.{file_extension}'
            # Get the individual file path of every file
            file_path = os.path.join(export_directory_path, file_name)
            # store the individual file path of every file in the list
            full_filename_list.append(Path(file_path))
    return full_filename_list


def _export_and_store_pages():
    """
    Export all the pages via BookStack API /api/pages/{page_id}/export/{filetype}
    :return:
    """
    page_info_dict = _read_file_and_store_info_in_dict()
    full_filename_list = _build_correct_export_path()

    for page_id, filename in zip(page_info_dict.keys(), full_filename_list):
        try:
            # try to download the exported page file in the expected format
            exported_page = session.get(f'{BOOKSTACK_URL}/api/pages/{page_id}/export/{EXPORT_TYPE}')

            # write the page.content (so bytecode) in the real file
            filename.write_bytes(exported_page.content)

            print(f'Successfully exported & stored file "{filename}".')
        except HTTPError as http_err:
            print(f'Oh, no! An HTTP Error occurred! Error: {http_err}')
        except Exception as err:
            print(f'Oh, no! An Error occurred! Error: {err}')


_export_and_store_pages()
