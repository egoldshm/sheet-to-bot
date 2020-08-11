##################################################################
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#                     eitntt@gmail.com                           #
##################################################################


from typing import *

from Configurations.data_spreadsheet_range_conf import RANGE_OF_COMMANDS
from Configurations.spreadsheet_id_conf import SPREADSHEET_ID
from bot_starter.botMenu import BotMenu
from file_reader.google_spreadsheep_reader import google_spreadsheet_reader

file_column = ["name", "type", "father_menu", "answer", "row", "column", "is_contact","disable_markdown","disable_web_page_preview", "back_to_main"]


def list_to_dict(row):
    result = {}
    for i in range(0, len(row)):
        result[file_column[i]] = row[i]
    for i in range(len(row), len(file_column)):
        result[file_column[i]] = ""
    return result


class data_to_bot:
    def __init__(self):
        self.spreadsheet_reader = google_spreadsheet_reader(SPREADSHEET_ID, RANGE_OF_COMMANDS)
        self.botMenu = BotMenu(self.get_data_from_file())

    def get_data_from_file(self) -> List[Dict[str, Union[str, Any]]]:
        """
        function that return dict of all the commands in the google spreadsheet

        :return:
        """

        if not self.spreadsheet_reader.values:
            raise Exception("Data not exist in the file with id '{}'".format(SPREADSHEET_ID))

        result = list(filter(lambda item: item["name"] != "", list(map(list_to_dict, self.spreadsheet_reader.values))))

        return result

