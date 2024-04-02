from lens35.settings import BASE_DIR
from util.logger import logger
import configparser
import traceback
import os

class PropertyReader:
    @staticmethod
    def get_property(section, key):
        try:
            config = configparser.ConfigParser()
            parent_dir = os.path.dirname(BASE_DIR)
            prop_file = "{}/lens_35.properties".format(parent_dir)
            config.read(prop_file)
            return config.get(section, key)
        except configparser.NoOptionError as e_0:
            logger.error('Failed to read {}.{} from property file. Reason : {}\n{}'.format(section, key, e_0, traceback.format_exc()))
            return None
