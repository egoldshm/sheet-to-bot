##################################################################
#                                                                #
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#               eitntt@gmail.com  - t.me/egoldshm                #
#                                                                #
##################################################################


import json
from typing import List, Dict

from Configurations.reports_filename_conf import FILENAME_registered_users, FILENAME_report
from Configurations.string_constants import SEND_MESSAGE_TO_ALL, MENU_LIST, RESET_MESSAGE, SEND_TO_USER, \
    DONE_FORM_MESSAGE, RECEIVED_MESSAGE_FORM
from bot_starter import User
from Configurations.bot_token_conf import CHANNEL_ID
from bot_starter.CommandNode import CommandNode
from bot_starter.Response import Response
from reporters.ReportFile import Report_to_file
from bot_starter.botMenu import RETURN_MENU_MESSAGE, RETURN_MESSAGE, RETURN_ONE_ASK, RETURN_ONE_MESSAGE
from bot_starter.data_to_tree import generate_commands_tree
from file_reader.getAdmins import getAdmins
from reporters.save_unique_in_file import Save_unique_in_file


def report_to_channel(bot, message, text, user, node) :
    try :
        bot.IsendMessage(CHANNEL_ID, """משתמש:
        {}
        הודעה 💬:
        {}
        תשובה 🗨:
        {}
        צומת 🌴:
        {}""".format(user, text, message, node), mark_down=False)
    except :
        print("Not find channel")


class Telegram_menu_bot :
    users_mode: Dict[int, CommandNode]
    tree: generate_commands_tree
    admins: List[int]

    def __init__(self) :
        self.tree = generate_commands_tree()
        self.users_mode = {}
        self.registered_users = Save_unique_in_file(FILENAME_registered_users)
        self.admins = getAdmins()
        self.file_reporter = Report_to_file(FILENAME_report)

    def messageHandler(self, chat_id, bot, user: User, text, message_id=None) -> str :
        try:
            if text in MENU_LIST :
                self.send_menu(bot, chat_id, text, user)
                return "MENU"

            keyboard = None
            if self.admin_menu(bot, chat_id, text, user) :
                return "ADMIN_MENU"

            # new user
            if user.id not in self.users_mode :
                self.users_mode[user.id] = self.tree.start_node

            # return message
            if text in (RETURN_MENU_MESSAGE, RETURN_ONE_ASK):
                if text == RETURN_MENU_MESSAGE :
                    keyboard = self.tree.start_node.keyboard
                    self.users_mode[user.id] = self.tree.start_node
                elif text == RETURN_ONE_ASK :
                    self.users_mode[user.id] = self.users_mode[user.id].parent if self.users_mode[user.id].parent else self.tree.start_node
                    keyboard = self.users_mode[user.id].keyboard
                message = RETURN_MENU_MESSAGE
                bot.IsendMessage(chat_id, message, keyboard=keyboard)
                self.report(bot, self.users_mode[user.id], message, text, user)
                return "BACK"

            if self.users_mode[user.id].form:
                if text == DONE_FORM_MESSAGE:
                    self.users_mode[user.id] = self.tree.start_node
                    message = RETURN_MENU_MESSAGE
                    bot.IsendMessage(chat_id, message, keyboard=self.tree.start_node.keyboard)
                else:
                    for admin in self.admins:
                        bot.Iforward_message(admin, chat_id, message_id)
                    bot.IsendMessage(chat_id, RECEIVED_MESSAGE_FORM ,keyboard=[[DONE_FORM_MESSAGE]])
                self.report(bot, self.users_mode[user.id],"", text, user)
                return "FORM"

            current_node = self.users_mode[user.id]

            # if we got /start -> back to main
            if text == self.tree.start_node.name:
                self.users_mode[user.id] = self.tree.start_node
                current_node = self.users_mode[user.id]
                keyboard = current_node.keyboard
                responses = self.tree.start_node.responses
            else :
                responses = self.tree.botMenu.responses_to_command(text, current_node)

            # check if this son:
            if text in current_node :
                new_node = current_node[text]
                keyboard = new_node.keyboard
                if new_node.children or new_node.form:
                    if new_node.form:
                        keyboard = [[DONE_FORM_MESSAGE]]
                    self.users_mode[user.id] = new_node

            else :
                self.users_mode[user.id] = self.tree.start_node

            message_to_report = self.send_response(bot, chat_id, responses, keyboard, user)

            self.report(bot, current_node, message_to_report, text, user)

            return "Done"
        except Exception as ex :
            if user and isinstance(user, User.User) :
                self.users_mode[user.id] = self.tree.start_node
            print(bot, user, text)
            print("ERROR (in messageHandler): " + str(ex))
            return "ERROR"

    def send_menu(self, bot, chat_id, text, user) :
        ROWS = 100
        message_to_send = str(self.tree)
        list_to_send = message_to_send.split("\n")
        for i in range(0, int(len(list_to_send) / ROWS) + 1) :
            bot.IsendMessage(chat_id, "\n".join(list_to_send[i * ROWS :min((i + 1) * ROWS, len(list_to_send))]))
        self.report(bot, self.users_mode[user.id], "<התפריט נשלח>", text, user)

    def report(self, bot, current_node: CommandNode, message_to_report: str, text: str, user: User.User) :
        report_to_channel(bot, message_to_report, text, user, str(current_node))
        self.file_reporter.addLine(user.id, user.f_name, user.l_name, user.username, text, message_to_report)
        self.registered_users.add_name(str(user.id))

    def send_response(self, bot, chat_id, responses: List[Response], keyboard=None, user=User.User()) :
        message_to_report = ""
        for response in responses :
            message = response.text
            message = user.replace_in_message(message)
            if response.message_type == "photo" :
                photo_id = response.data_id
                bot.IsendPhoto(chat_id, photo_id, message, keyboard=keyboard, inline_keyboard=response.inline_keyboard,
                               mark_down=response.mark_down)
            elif response.message_type == "file" :
                file_id = response.data_id
                bot.IsendFile(chat_id, file_id, message, keyboard=keyboard, inline_keyboard=response.inline_keyboard,
                              mark_down=response.mark_down)
            elif response.message_type == "sticker" :
                file_id = response.data_id
                bot.IsendSticker(chat_id, file_id, message)
            else :
                bot.IsendMessage(chat_id, message, keyboard=keyboard, inline_keyboard=response.inline_keyboard,
                                 mark_down=response.mark_down,
                                 disable_web_preview=not response.link_preview)
            message_to_report += "| {}".format(message)
        return message_to_report

    def admin_menu(self, bot, chat_id: int, text: str, user: User.User) :
        # admin menu:
        if user.id in self.admins :
            if text[0] == '{' :
                message = json.dumps(text, indent=1)

            # reset the commands in the bot
            elif text == RESET_MESSAGE :
                self.tree.__init__()
                for user_id in self.users_mode.keys() :
                    if self.users_mode[user_id].name == "/start" :
                        self.users_mode[user_id] = self.tree.start_node
                    self.users_mode[user.id] = self.tree.start_node
                message = "התפריט אופס בהצלחה! 👌 "


            # send message to all
            elif SEND_MESSAGE_TO_ALL in text :
                text_to_send = text.replace(SEND_MESSAGE_TO_ALL, "")
                responses = None
                if text_to_send in self.tree.botMenu.global_commands :
                    responses = self.tree.botMenu.global_commands[text_to_send]

                count = 0
                for user_id in self.registered_users.data :
                    try :
                        if responses :
                            self.send_response(bot, user_id, responses)
                        else :
                            bot.IsendMessage(user_id, text_to_send)
                        count += 1
                    except :
                        pass
                message = "ההודעה נשלחה בהצלחה ל{} משתמשים".format(count)

            #  send private massage
            elif SEND_TO_USER in text :
                text_to_send = text.replace(SEND_TO_USER, "")
                list_of_message = text_to_send.split("\n")
                user_id = list_of_message[0]
                if not user_id.isdigit() :
                    return False
                user_id = int(user_id)
                text_to_send = "\n".join(list_of_message[1 :])
                responses = None
                if text_to_send in self.tree.botMenu.global_commands :
                    responses = self.tree.botMenu.global_commands[text_to_send]
                try :
                    if responses :
                        self.send_response(bot, user_id, responses)
                    else :
                        bot.IsendMessage(user_id, text_to_send)
                    message = "ההודעה נשלחה בהצלחה ל{}".format(user_id)
                except :
                    message = "לא הצלחתי לשלוח הודעה ל{}".format(user_id)
            else :
                return False
            bot.IsendMessage(chat_id, message, keyboard=self.tree.start_node.keyboard, mark_down=False)
            return True
