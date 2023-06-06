from lens35.settings import BASE_DIR
import configparser
import os

class PropertyReader:
    @staticmethod
    def get_property(section, key):
        config = configparser.ConfigParser()
        parent_dir = os.path.dirname(BASE_DIR)
        prop_file = "{}/lens_35.properties".format(parent_dir)
        config.read(prop_file)
        try:
            return config.get(section, key)
        except configparser.NoOptionError:
            return None
