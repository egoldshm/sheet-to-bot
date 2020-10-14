##################################################################
#                                                                #
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#               eitntt@gmail.com  - t.me/egoldshm                #
#    #        השימוש ללא אישור אסור לפי ההלכה ולפי הרישיון והחוק הבינלאומי
#                                                                #
##################################################################

from typing import List, Dict, Optional, Tuple

from bot_starter.CommandNode import CommandNode
from bot_starter.Response import Response
from Configurations.string_constants import *


def splitMessage(message: str) -> Tuple[str, str] :
    """
    function that get response of photo or file - and return two part - the file id and and the text

    :return: (file id, caption)
    """
    split_list = message.split(" ")
    if len(split_list) > 1 :
        return split_list[0], " ".join(split_list[1 :])
    return message, ""


def create_response(res: Dict) -> Response :
    """
    get dict of format got in "values to bot" -> and convert to Response type

    :rtype: Response
    """
    if res["type"].upper() not in ("TEXT", "TXT", "") :
        data_id, message = splitMessage(res["answer"])
        r = Response(message, link_preview=res["disable_web_page_preview"] != "TRUE",
                     mark_down=res["disable_markdown"] != "TRUE",
                     is_contact=res["is_contact"] == "TRUE", message_type=res["type"], data_id=data_id)
    elif res["type"].upper() == "FORM" :
        r = Response(res["answer"], link_preview=res["disable_web_page_preview"] != "TRUE",
                     mark_down=res["disable_markdown"] != "TRUE",
                     is_contact=res["is_contact"] == "TRUE", message_type=res["type"])
    else :
        r = Response(res["answer"], link_preview=res["disable_web_page_preview"] != "TRUE",
                     mark_down=res["disable_markdown"] != "TRUE", is_contact=res["is_contact"] == "TRUE")

    inline_keyboard: str = res["inline_keyboard"]
    result_inline_keyboard = []
    if inline_keyboard != "" :
        try :
            list_of_rows = inline_keyboard.split("\n")
            for row in list_of_rows :
                list_of_items = row.split("|")
                result_for_line = []
                for item in list_of_items :
                    text = item.split("-")[0].strip()
                    # todo: add check to format and url
                    url = "-".join(item.split("-")[1:]).strip()
                    result_for_line.append((text, url))
                result_inline_keyboard.append(result_for_line)
            r.inline_keyboard = result_inline_keyboard
        except :
            print("problem with parse inline keyboard - " + inline_keyboard)
            print("result: " + str(result_inline_keyboard) + " | " + str(result_for_line))
    return r


class BotMenu :
    command: List[Dict]
    global_commands: Dict[str, Tuple[List[Response], Optional[List[List[str]]]]]
    contacts: List[Tuple[str, str]]

    def __init__(self, commands: List[dict]) :
        self.commands = list(filter(lambda i : i, commands))
        self.global_commands = self.reset_global_commands()
        self.contacts = self.reset_contacts()

    def reset_global_commands(self, all_commands_is_global: bool = True) -> Dict[str, Tuple[List[Response], Optional[List[List[str]]]]] :
        """
        found all commands that hasn't father - and become to global commands

        :return: dict of "name of command" => "response"
        """
        keyboard: List[List[str]]
        already_inserted = []
        result_dict = {}
        for command in self.commands :
            name = command["name"]
            if name not in already_inserted and (command["father_menu"] == "" or all_commands_is_global) :
                commands_by_father_name = list(
                    filter(
                        lambda i : (i["father_menu"] == "" or all_commands_is_global) and i["name"] == name,
                        self.commands))
                responses = []
                for res in commands_by_father_name :
                    responses.append(create_response(res))
                already_inserted.append(name)
                keyboard = self.menu_by_father(name)
                if keyboard:
                    keyboard.append([RETURN_MENU_MESSAGE])
                result_dict[name] = (responses, keyboard)
        return result_dict

    def reset_contacts(self) -> List[Tuple[str, str]] :
        return list(
            map(lambda com : (com["name"], com["answer"]), filter(lambda i : i["is_contact"] == 'TRUE', self.commands)))

    def responses_to_command(self, text: str, node: CommandNode) -> List[Response] :
        response_as_result: str

        if text in node :
            return node[text].responses

        # search in global commands
        if text in self.global_commands :
            return self.global_commands[text][0]

        # contacts -> text only:
        response_as_result = self.get_responses_for_contacts(text)

        if not response_as_result:
            return [Response(COMMAND_NOT_FOUND_MESSAGE)]
        return [Response(response_as_result)]

    def menu_return(self, menu_name) -> Optional[str] :
        fathers = list(filter(lambda i : i["name"] == menu_name, self.commands))
        if len(fathers) == 0 :
            return None
        father_menu = fathers[0]["father_menu"]
        return father_menu

    def get_responses_for_contacts(self, text) -> str:
        result = []
        for input_message, response in self.contacts :
            if input_message == text :
                return response
            else :
                list_of_spilt = input_message.strip().split(" ")
                for j in list_of_spilt :
                    if j in text.split(" ") and len(j) > 1 and j not in IGNORE_WORDS :
                        if input_message in text :
                            return response
                        else :
                            if response not in result:
                                result.append(response)
        if result:
            return WHAT_WE_FOUND_MESSAGE + LIST_OF_ITEMS_FOUND_SIGN + "\n{} ".format(LIST_OF_ITEMS_FOUND_SIGN).join(
                    result)


    def menu_by_father(self, father_name="/start"):

        # take only command that father_menu is father name
        commands_for_menu = list(filter(lambda i : i["father_menu"] == father_name, self.commands))

        # remove duplicates
        temp_commands_for_menu = []
        for i in commands_for_menu :
            if i["name"] not in map(lambda j : j["name"], temp_commands_for_menu) :
                temp_commands_for_menu.append(i)
        commands_for_menu = temp_commands_for_menu

        left_buttons = []

        # get the rows of the commands
        rows_list = list(map(lambda i : int(i["row"]) if i["row"].isdigit() else 0, commands_for_menu))

        if not rows_list :
            return None

        max_row = max(rows_list)
        buttons = []
        for i in range(max_row + 1) :
            columns = [int(j["column"]) for j in commands_for_menu if j["row"] == str(i)]
            max_column = max([1] if columns == [] else columns)
            buttons.append(["" for j in range(max_column + 1)])
        for i in commands_for_menu :
            if not i["row"].isdigit() or not i["column"].isdigit() :
                left_buttons.append(i["name"])
            else :
                buttons[int(i["row"])][int(i["column"])] = i["name"]
        for i in left_buttons :
            buttons.append([i])

        return buttons
