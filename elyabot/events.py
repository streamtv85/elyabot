import html
import os
import random
import re
from time import sleep

import arrow as arrow
import emoji
import requests
import telegram
from urllib.parse import urlencode
import logging

logger = logging.getLogger('bot-service.events')


def start(bot, update):
    debug_info(bot, update)
    text = "I'm ELYA bot, how can I help you?"
    event_info("START command", update, text)
    bot.send_message(chat_id=update.message.chat_id, text=text)


def unknown(bot, update):
    debug_info(bot, update)
    reply = "Sorry, I didn't understand that command."
    event_info("Unknown command", update, reply)
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def welcome(bot, update):
    debug_info(bot, update)
    message = "Welcome to the chat!"
    bot.send_message(chat_id=update.message.chat_id, text=message)


def debug_info(bot, update):
    logger.debug(' > received message from chat id: ' + str(update.message.chat_id))
    logger.debug(' > from user: ' + str(update.message.from_user))
    logger.debug(' > message text: ' + str(update.message.text))
    logger.debug(
        ' > chat member info: ' + str(bot.get_chat_member(update.message.chat_id, update.message.from_user.id)))


def event_info(prefix, update, message):
    if message:
        suffix = "Response:\n"
    else:
        suffix = ""
    logger.info(
        prefix + ": chat id {0!s}, user {1} ({2}). ".format(
            update.message.chat_id, update.message.from_user.username if update.message.from_user.username else (
                    update.message.from_user.first_name + update.message.from_user.last_name),
            update.message.from_user.id) + suffix + message)
