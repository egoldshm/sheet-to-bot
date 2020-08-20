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

import telepot
import urllib3
from flask import Flask, request
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from Configurations.bot_token_conf import TOKEN
from Configurations.pythonanywhere_conf import PYTHONANYWHERE_NAME
from bot_starter.MessageHandler import Telegram_menu_bot
from bot_starter.User import User

secret = "7bd8040d-baff-41c2-b16f-cdffb6e168f0"

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default' : urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(TOKEN)
bot.setWebhook("https://{}.pythonanywhere.com/{}".format(PYTHONANYWHERE_NAME, secret), max_connections=1)

app = Flask(__name__)


def list_of_lists_to_keyboards(buttons: List[List[str]]) :
    return ReplyKeyboardMarkup(keyboard=buttons)


def list_of_lists_to_inline_keyboard(buttons: List[List[Tuple[str, str]]]) :
    if not buttons :
        return None
    for i in range(len(buttons)) :
        for j in range(len(buttons[i])) :
            item = buttons[i][j]
            buttons[i][j] = InlineKeyboardButton(text=item[0], url=item[1])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


class flaskBot :
    def __init__(self, bot_p) :
        self.bot = bot_p

    def IsendMessage(self, chat_id, message, keyboard=None, mark_down=True, inline_keyboard=None,
                     disable_web_preview=None) :
        keyboard = self.get_valid_keyboard(keyboard)
        inline_keyboard = list_of_lists_to_inline_keyboard(inline_keyboard)
        self.bot.sendMessage(chat_id, message, reply_markup=keyboard if keyboard else inline_keyboard,
                             parse_mode='Markdown' if mark_down else "HTML",
                             disable_web_page_preview=disable_web_preview)

    def IsendFile(self, chat_id, file_id, text=None, keyboard=None, mark_down=True, disable_web_preview=None,
                  inline_keyboard=None) :
        keyboard = self.get_valid_keyboard(keyboard)
        inline_keyboard = list_of_lists_to_inline_keyboard(inline_keyboard)
        self.bot.sendDocument(chat_id, file_id, caption=text, parse_mode='Markdown' if mark_down else "HTML",
                              reply_markup=keyboard if keyboard else inline_keyboard)

    def IsendPhoto(self, chat_id, photo_id, text=None, keyboard=None, mark_down=True, inline_keyboard=None) :
        keyboard = self.get_valid_keyboard(keyboard)
        inline_keyboard = list_of_lists_to_inline_keyboard(inline_keyboard)
        self.bot.sendPhoto(chat_id, photo_id, caption=text, parse_mode='Markdown' if mark_down else "HTML",
                           reply_markup=keyboard if keyboard else inline_keyboard)

    def IsendSticker(self, chat_id, sticker_id, keyboard=None, **kwargs) :
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.sendSticker(chat_id, sticker_id, reply_markup=keyboard)

    def Iforward_message(self, chat_id, from_chat_id, message_id) :
        bot.forwardMessage(chat_id, from_chat_id, message_id)

    def get_valid_keyboard(self, keyboard) :
        if keyboard and not isinstance(keyboard, str) :
            keyboard = list_of_lists_to_keyboards(keyboard)
        else :
            keyboard = None
        return keyboard


telegram_menu_bot = Telegram_menu_bot()
count = 0


@app.route('/{}'.format(secret), methods=["POST"])
def answer():
    global user
    global count
    user = None
    message_id = None
    mybot = flaskBot(bot)
    count = count + 1
    update = request.get_json()

    try :
        if "message" not in update :
            print("problem with 'message'")
            print(str(update))
        message = update["message"]
        print("message{}: {}".format(count, message))
        if "text" not in message :
            print("problem with 'text'")
            print(str(message))
        if "chat" not in message :
            print("problem with chat")
            print(str(message))

        chat = message["chat"]
        chat_id = chat["id"]
        user = message["from"]

        message_id = message["message_id"]

        text = message["text"]
    except :
        print(update)
        text = str(update)
    if user :
        user = User(user["id"], user.get("first_name"), user.get("last_name"), user.get("user_name"))
        return telegram_menu_bot.messageHandler(chat_id, mybot, user, text, message_id=message_id)
    return "ERROR"
