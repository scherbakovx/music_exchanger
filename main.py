# -*- coding: utf-8 -*-
import json
from typing import Tuple
import telebot
from dbhelper import DBHelper
from utils import validate_playist_url


data = json.loads(open('bot_data.json', 'r').read())
bot_token = data['token']

bot = telebot.TeleBot(bot_token)

db = DBHelper()
db.setup()

def handle_playlist_url_from_user(url: str = "", user_id: int = 1) -> str:
    success, error_message = validate_playist_url(url)
    if success:
        if db.check_if_user_could_add_playlist_url(user_id):
            db.add_playlist_url_from_user(url, user_id)
            return "Готово! Уверен, кому-то понравится твоя музыка :)"
        else:
            return "Нельзя добавлять больше одного плейлиста в день!"
    else:
        return error_message

def handle_request_for_playlist_url_from_user(user_id: int) -> Tuple[bool, str]:
    if db.check_if_user_could_get_playlist_url(user_id):
        playlist_url = db.get_random_playlist_url_for_user(user_id)
        if playlist_url:
            return True, playlist_url
        else:
            return False, "У меня нет для тебя плейлиста, но попробуй вернуться позже!"
    return False, "Ты можешь запросить только один плейлист в день!"

@bot.message_handler(commands=['start', 'help'])
def handle_start_command(message):
    bot.reply_to(message, "Сейчас я напишу инструкцию и всё будет кайф!")

@bot.message_handler(commands=['get'])
def handle_get_command(message):
    user_id = message.from_user.id
    success, result = handle_request_for_playlist_url_from_user(user_id)
    if success:
        message = bot.reply_to(message, "Вот тебе небольшой плейлист на сегодня: %s" % result)
        db.add_info_about_requested_url(result, user_id, message.id)
    else:
        bot.reply_to(message, result)

@bot.message_handler(func=lambda m: True)
def handle_usual_messages(message):
    user_id = message.from_user.id
    text = message.text
    answer_text = handle_playlist_url_from_user(text, user_id)
    bot.reply_to(message, answer_text)

bot.infinity_polling()
