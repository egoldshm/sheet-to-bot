##################################################################
#                                                                #
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#               eitntt@gmail.com  - t.me/egoldshm                #
#    #      השימוש ללא אישור אסור לפי ההלכה ולפי הרישיון והחוק הבינלאומי  
#                                                                #
##################################################################

import telebot
from telebot import types

from bot_starter.MessageHandler import Telegram_menu_bot
from bot_starter.User import User

bot = telebot.TeleBot("581353633:AAGfgfRpPCVUI_qRal9KUYVNQPPOo5Dbia4")


def list_of_lists_to_keyboards(buttons):
    markup = types.ReplyKeyboardMarkup()
    for row in buttons:
        list_of_buttons = []
        for item in row:
            list_of_buttons.append(types.KeyboardButton(item))
        markup.add(*list_of_buttons)
    return markup


class TelepbotBot:
    def __init__(self, bot_p):
        self.bot = bot_p

    def IsendMessage(self, chat_id, message, keyboard=None, mark_down=True, inline_keyboard=None, disable_web_preview=False):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.send_message(chat_id, message, parse_mode='Markdown' if mark_down else None, reply_markup=keyboard if keyboard else inline_keyboard,
                              disable_web_page_preview=disable_web_preview)

    def IsendFile(self, chat_id, file_id, text=None, keyboard=None, inline_keyboard=None, mark_down=True):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.send_document(chat_id, file_id, caption=text, reply_markup=keyboard if keyboard else inline_keyboard,
                               parse_mode='Markdown' if mark_down else None)

    def IsendPhoto(self, chat_id, photo_id, text, keyboard=None, inline_keyboard=None, mark_down=True):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.send_photo(chat_id, photo_id, caption=text, reply_markup=keyboard if keyboard else inline_keyboard,
                            parse_mode='Markdown' if mark_down else None)

    def IsendSticker(self, chat_id, sticker_id, keyboard=None, **kwargs):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.send_sticker(chat_id, sticker_id, reply_markup=keyboard)

    def get_valid_keyboard(self, keyboard):
        if keyboard and not isinstance(keyboard, str):
            keyboard = list_of_lists_to_keyboards(keyboard)
        else:
            keyboard = None
        return keyboard


telegram_menu_bot = Telegram_menu_bot()


@bot.message_handler(func=lambda message: True,
                     content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact',
                                    'sticker'])
def answer(update):
    telepbotBot = TelepbotBot(bot)
    chat = update.chat
    chat_id = chat.id
    text = update.text

    user = update.from_user
    print(user)
    user_p = User(user.id, user.first_name, user.last_name, user.username)

    return telegram_menu_bot.messageHandler(chat_id, telepbotBot, user_p, text)


bot.polling()
