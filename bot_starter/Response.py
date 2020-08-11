##################################################################
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#                     eitntt@gmail.com                           #
##################################################################


class Response:
    text: str
    link_preview: bool
    mark_down: bool
    message_type: str
    data_id: str

    def __init__(self, text:str, link_preview=True, mark_down=True, message_type="text", is_contact = False,  data_id=""):
        self.link_preview = link_preview
        self.mark_down = mark_down
        self.message_type = message_type
        self.data_id = data_id
        self.is_contact = is_contact
        self.text = text

    def __str__(self) -> str:
        return "{} ({}, {}) {}".format(self.text, self.link_preview, self.mark_down,
                                       "" if self.message_type == "text" else self.message_type + "(" + self.data_id + ")")
