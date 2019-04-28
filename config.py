import datetime
import logging
import os

TEMPLATE_FILE_NAME = 'product-template.csv'


def root_dir():
    return os.path.dirname(os.path.abspath(__file__)) + '/'


def resource_dir():
    return root_dir() + 'resources/'


def csv_template_dir():
    return resource_dir() + 'csv-template/'


logger = logging.getLogger()


def logging_config():
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(
        '{0}/{1}.log'.format(resource_dir(), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    log_formatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    logger.debug('Finish logger configuration setup')


def initialise_configurations():
    logging_config()
    logger.info('Finish configuration initialisation')
