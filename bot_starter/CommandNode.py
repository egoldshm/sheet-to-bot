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
    form: str

    def __init__(self, name="/start", responses:List[Response]=None, parent=None, children=None, keyboard=None, **kwargs):
        super().__init__(name, parent, children, **kwargs)
        self.set_responses(responses)
        self.keyboard = keyboard

    def set_responses(self, responses:List[Response]):
        if responses:
            self.form = self.name if any(map(lambda i: i.message_type == "form", responses)) else ""
        self.responses = responses

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

    def __str__(self):
        return """שם: {}
        מקלדת: {}
        """.format(self.name if not self.parent else self.name + """
        אבא:{}""".format(self.parent.name), self.keyboard)
