import csv

from src.Config import csv_template_dir, TEMPLATE_FILE_NAME, logger
from src.domain.ShoppifyCsv import ShoppifyCsv


def append_csv_row(csv_file_path, shoppifyCsv: ShoppifyCsv):
    with open(csv_file_path, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(shoppifyCsv.__dict__.values())
        logger.debug('Inserted row to csv: {}'.format(shoppifyCsv.__dict__.values()))


def test():
    append_csv_row(csv_template_dir() + TEMPLATE_FILE_NAME, ShoppifyCsv())


test()
