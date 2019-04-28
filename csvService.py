import csv
import shutil

from config import logger


def append_csv_array_to_file(csv_file_path: str, shoppify_csv_array: list):
    with open(csv_file_path, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for csv_row in shoppify_csv_array:
            writer.writerow(csv_row.__dict__.values())
            logger.debug('Inserted in to csv file {} row: {}'.format(csv_file.name, csv_row.__dict__.values()))


def clean_csv_file(csv_template_file_path: str, csv_file_path: str):
    shutil.copyfile(csv_template_file_path, csv_file_path)
    logger.debug('Cleaned file: {}'.format(csv_template_file_path))
