import datetime
import logging
import os

TEMPLATE_FILE_NAME = 'johnson-hardwood-template.csv'


def root_dir():
    return os.path.dirname(os.path.abspath(__file__ + '../../')) + '/'


def resource_dir():
    return root_dir() + 'resources/'


def log_dir():
    return resource_dir() + 'log/'


def csv_template_dir():
    return resource_dir() + 'csv-template/'


logger = logging.getLogger()


def logging_config():
    logger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(
        '{0}/{1}.log'.format(log_dir(), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    # logger.addHandler(consoleHandler)
    logger.debug('Finish logger configuration setup')


def initialise_configurations():
    logging_config()
    logger.info('Finish configuration initialisation')
