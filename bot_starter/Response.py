##################################################################
#                                                                #
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#               eitntt@gmail.com  - t.me/egoldshm                #
#    #      השימוש ללא אישור אסור לפי ההלכה ולפי הרישיון והחוק הבינלאומי  
#                                                                #
##################################################################
from typing import List, Tuple


class Response:
    text: str
    link_preview: bool
    mark_down: bool
    message_type: str
    data_id: str
    inline_keyboard: List[List[Tuple[str, str]]]

    def __init__(self, text:str, link_preview=True, mark_down=True, message_type="text", is_contact = False,  data_id="", inline_keyboard: List[List[Tuple[str, str]]] = None):
        self.inline_keyboard = inline_keyboard
        self.link_preview = link_preview
        self.mark_down = mark_down
        self.message_type = message_type
        self.data_id = data_id
        self.is_contact = is_contact
        self.text = text

    def __str__(self) -> str:
        return "{} ({}, {}) {} inline: {}".format(self.text, self.link_preview, self.mark_down,
                                       "" if self.message_type == "text" else self.message_type + "(" + self.data_id + ")", self.inline_keyboard)
