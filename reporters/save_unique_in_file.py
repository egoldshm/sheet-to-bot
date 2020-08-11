##################################################################
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#                     eitntt@gmail.com                           #
##################################################################

import os
from typing import List, Any


class Save_unique_in_file:
    data: List[str]

    def __init__(self, file_name):
        self.data = []
        self.file_name = file_name
        if not os.path.isfile(file_name):
            file = open(file_name, "w")
            file.close()
        else:
            file = open(file_name, "r")
            self.data = list(map(lambda s: s.strip(), file.readlines()))
            file.close()

    def name_exist(self, name: str) -> bool:
        return str(name) in self.data

    def add_name(self, name: str):
        if not self.name_exist(name):
            self.data.append(name)
            file = open(self.file_name, "a")
            file.write(name + "\n")
            file.close()
