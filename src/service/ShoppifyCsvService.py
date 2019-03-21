import csv
from src.Config import logger
from src.model.ShoppifyCsv import ShoppifyCsv


def append_csv_row(csv_file_path: str, shoppifyCsv: ShoppifyCsv):
    with open(csv_file_path, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(shoppifyCsv.__dict__.values())
        logger.debug('Inserted row to csv: {}'.format(shoppifyCsv.__dict__.values()))
