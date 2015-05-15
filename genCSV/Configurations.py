#_author__ = 'Thomas'


class Configurations:

    def __init__(self, config_full_name):
        self.config_name = config_full_name

    def config_name(self):
        return self.config_name

    @staticmethod
    def parser_final():
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('Config.ini')
        parser_finals = parser.get('file_path', 'common_base_path')
        return parser_finals
        #print(parser.get('file_path', 'common_base_path'))

    @staticmethod
    def get_file_endings(tool):
        from configparser import ConfigParser
        parser = ConfigParser()
        config_variable = "synopsys"
        if tool == 'cadence':
            config_variable = 'cadence'
        parser.read('Config.ini')
        file_name_list = parser.get('file_endings', config_variable)
        return file_name_list