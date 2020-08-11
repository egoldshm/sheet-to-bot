##################################################################
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#                     eitntt@gmail.com                           #
##################################################################

from typing import List

from anytree import Node

from bot_starter.Response import Response


class CommandNode(Node):
    keyboard: List[List[str]]
    responses: List[Response]

    def __init__(self, name="/start", responses=None, parent=None, children=None, keyboard=None, **kwargs):
        super().__init__(name, parent, children, **kwargs)
        self.keyboard = keyboard
        self.responses = responses

    responses: List
    keyboard: List[List[str]]

    def __contains__(self, item: str):
        for sub_command in self.children:
            if item == sub_command.name:
                return True
        return False

    def __getitem__(self, item):
        if item in self:
            for sub_command in self.children:
                if item == sub_command.name:
                    return sub_command
        return None
