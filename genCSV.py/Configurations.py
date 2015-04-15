#__author__ = 'Thomas'


class Configurations:

    @staticmethod
    def parser_final():
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('Config.ini')
        parser_finals = parser.get('file_path', 'common_base_path')
        return parser_finals
        #print(parser.get('file_path', 'common_base_path'))

    @staticmethod
    def get_file_endings():
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('Config.ini')
        file_name_list = parser.get('file_endings', 'fileNames')
        return file_name_list