##################################################################
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#                     eitntt@gmail.com                           #
##################################################################


from Configurations.admin_spreadsheet_range_conf import RANGE_OF_ADMINS
from Configurations.spreadsheet_id_conf import SPREADSHEET_ID
from file_reader.google_spreadsheep_reader import google_spreadsheet_reader
from typing import List


def getAdmins() -> List[int] :
    reader = google_spreadsheet_reader(SPREADSHEET_ID, RANGE_OF_ADMINS)
    values = list(map(lambda i : int(i[0]), reader.values))
    return values
