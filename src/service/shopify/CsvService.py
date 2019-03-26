import csv

from src.Config import logger


def append_csv_array_to_file(csv_file_path: str, shoppify_csv_array: list):
    with open(csv_file_path, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for csv_row in shoppify_csv_array:
            writer.writerow(csv_row.__dict__.values())
            logger.debug('Inserted row to csv: {}'.format(csv_row.__dict__.values()))
