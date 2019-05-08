import os

from config import logger


def write_url_list_to_file(url_file_path: str, urls: list):
    with open(url_file_path, 'a') as url_file:
        for url in urls:
            url_file.writelines(url + '\n')
            logger.debug('Inserted in to url text file {} row: {}'.format(url_file.name, url))


def read_url_list_from_file(url_file_path: str):
    with open(url_file_path, 'r') as url_file:
        logger.debug('Reading file {} lines'.format(url_file.name))
        return url_file.readlines()


def is_url_file_empty(url_file_path: str):
    return os.stat(url_file_path).st_size == 0 if os.path.isfile(url_file_path) else True


def delete_lines_in_url_file(url_file_path: str, lines_number: int):
    url_file = open(url_file_path, 'r')
    lines = url_file.readlines()[lines_number:]
    url_file.close()
    url_file = open(url_file_path, 'w')
    url_file.writelines(lines)
    url_file.close()
