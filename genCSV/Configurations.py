#__author__ = 'Thomas'


class Configurations:

    def parser_final(self):
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('Config.ini')
        parser_finals = parser.get('file_path', 'common_base_path')
        return  parser_finals
        #print(parser.get('file_path', 'common_base_path'))