# -*- coding: utf-8 -*-
import os
import time

import flask
import telebot
import psycopg2

from config import API_TOKEN, WEBHOOK_LISTEN, WEBHOOK_PORT, WEBHOOK_HOST, CHAT_ID
from db import increment_karma


WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return '<h1>Ninja karma</h1>'


@app.route(WEBHOOK_URL_PATH, methods=['POST', 'GET'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8') 
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'def webhook():'
    else:
        flask.abort(403)


@bot.message_handler(commands=['start', 's', 'info', 'i'])
def start(message):
    pass


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    if message.chat.id != CHAT_ID:
        return
    if message.reply_to_message is not None:
        if message.text in ['+', 'спасибо']:
            username = message.reply_to_message.from_user.username,
            username = username[0]
            if username != message.from_user.username:
                bot.send_message(
                    CHAT_ID,
                    'Репутация @%s: %s' % (
                        username, 
                        increment_karma(username)
                    )
                )

bot.remove_webhook()
time.sleep(3)
bot.set_webhook(url='https://%s' % WEBHOOK_HOST + WEBHOOK_URL_PATH)
if __name__ == '__main__':
    _port = int(os.environ.get('PORT', WEBHOOK_PORT))
    app.run(
        host=WEBHOOK_LISTEN,
        port=_port,
        debug=True
    )
