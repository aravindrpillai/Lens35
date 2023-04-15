import configparser

class PropertyReader:
    @staticmethod
    def get_property(section, key):
        config = configparser.ConfigParser()
        config.read("C:/lens_35.properties")
        try:
            return config.get(section, key)
        except configparser.NoOptionError:
            return None
