##################################################################
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#                     eitntt@gmail.com                           #
##################################################################

from typing import List

import telepot
import urllib3
from flask import Flask, request
from telepot.namedtuple import ReplyKeyboardMarkup

from Configurations.bot_token_conf import TOKEN
from Configurations.pythonanywhere_conf import PYTHONANYWHERE_NAME
from bot_starter.MessageHandler import Telegram_menu_bot
from bot_starter.User import User

secret = "7bd8040d-baff-41c2-b16f-cdffb6e168f0"

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(TOKEN)
bot.setWebhook("https://{}.pythonanywhere.com/{}".format(PYTHONANYWHERE_NAME, secret), max_connections=1)

app = Flask(__name__)


def list_of_lists_to_keyboards(buttons: List[List[str]]):
    return ReplyKeyboardMarkup(keyboard=buttons)


class flaskBot:
    def __init__(self, bot_p):
        self.bot = bot_p

    def IsendMessage(self, chat_id, message, keyboard=None, mark_down=True, disable_web_preview=None):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.sendMessage(chat_id, message, reply_markup=keyboard, parse_mode='Markdown' if mark_down else None, disable_web_page_preview=disable_web_preview)

    def IsendFile(self, chat_id, file_id, text=None, keyboard=None, mark_down=True, disable_web_preview=None):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.sendDocument(chat_id, file_id, caption=text, parse_mode='Markdown' if mark_down else None, reply_markup=keyboard)

    def IsendPhoto(self, chat_id, photo_id, text=None, keyboard=None, mark_down=True):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.sendPhoto(chat_id, photo_id, caption=text, parse_mode='Markdown' if mark_down else None, reply_markup=keyboard)

    def IsendSticker(self, chat_id, sticker_id, keyboard=None, **kwargs):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.sendSticker(chat_id, sticker_id, reply_markup=keyboard)

    def IsendPolling(self):
        pass

    def get_valid_keyboard(self, keyboard):
        if keyboard and not isinstance(keyboard, str):
            keyboard = list_of_lists_to_keyboards(keyboard)
        else:
            keyboard = None
        return keyboard


telegram_menu_bot = Telegram_menu_bot()


@app.route('/{}'.format(secret), methods=["POST"])
def answer():
    global user
    user = None
    mybot = flaskBot(bot)

    update = request.get_json()
    try:
        if "message" not in update:
            print("problem with 'message'")
            print(str(update))
        message = update["message"]
        if "text" not in message:
            print("problem with text")
            print(str(message))
        if "chat" not in message:
            print("problem with chat")
            print(str(message))

        chat = message["chat"]
        chat_id = chat["id"]
        user = message["from"]

        text = message["text"]
    except:
        print(update)
        text = str(update)
    if user:
        user = User(user["id"], user.get("first_name"), user.get("last_name"), user.get("user_name"))
        return telegram_menu_bot.messageHandler(chat_id, mybot, user, text)
    return "ERROR"

