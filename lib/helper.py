# coding: UTF-8

from pprint import pprint

import logging
import logging.config
import inspect
import os

script_path = os.path.dirname(os.path.abspath(inspect.currentframe().f_code.co_filename))
logging.config.fileConfig(script_path + '/../logger.conf', disable_existing_loggers=True)
logger = logging.getLogger('mylogger')
