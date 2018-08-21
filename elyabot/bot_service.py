#!/usr/bin/env python3

import logging
import os
import sys
import emoji
from logging.handlers import TimedRotatingFileHandler
from threading import Thread
from telegram import ParseMode
from telegram.ext import MessageHandler, Filters, Updater, CommandHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

from elyabot import events, StocksExchangeWatcher
from elyabot.configmanager import config

cwd = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('bot-service')
log_level = config.get('logLevel')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
logfilename = os.path.join(cwd, 'bot-service.log')
logdebugfilename = os.path.join(cwd, 'bot-service-debug.log')
fh = TimedRotatingFileHandler(logfilename, when='D', interval=1, backupCount=int(config.get('logMaxAge')),
                              encoding='utf_8')
fh.setLevel(logging.getLevelName(log_level))
fhdebug = TimedRotatingFileHandler(logdebugfilename, when='D', interval=1, backupCount=3, encoding='utf_8')
fhdebug.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.getLevelName(log_level))
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
fhdebug.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(fhdebug)
logger.addHandler(ch)

# exmo_watcher = ExchangeWatcher('exmo', 'BTC/USD')
# bitfin_watcher = ExchangeWatcher('bitfinex', 'BTC/USD')
el = StocksExchangeWatcher()


def send_prices(bot, update):
    global el
    price = el.get_price()
    # logger.debug("got price: {}".format(price))
    message = "<b>ELYA</b> price: {0} BTC".format(price)
    events.event_info("Price request", update, message)
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.HTML)


def add_message_handlers(disp):
    logger.info("Adding message handlers.")
    welcome_handler = MessageHandler(Filters.status_update.new_chat_members, events.welcome)
    disp.add_handler(welcome_handler)


def add_command_handlers(disp):
    logger.info("Adding command handlers.")
    start_handler = CommandHandler('start', events.start)
    disp.add_handler(start_handler)

    prices_handler = CommandHandler('price', send_prices)
    disp.add_handler(prices_handler)

    w_handler = CommandHandler('welcome', events.welcome)
    disp.add_handler(w_handler)

    # should be added as the LAST handler
    unknown_handler = MessageHandler(Filters.command, events.unknown)
    disp.add_handler(unknown_handler)


def error_callback(bot, update, error):
    # for the future - if we need to handle any specific Telegram exceptions
    try:
        raise error
    except Unauthorized:
        pass
        # remove update.message.chat_id from conversation list
    except BadRequest:
        pass
    # handle malformed requests - read more below!
    except TimedOut:
        pass
    # handle slow connection problems
    except NetworkError:
        pass
    # handle other connection problems
    except ChatMigrated as e:
        pass
    # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
    # handle all other telegram related errors


# main entry point, executed when the file is being run as a script
def main():
    logger.info("Current folder is: " + cwd)
    updater = Updater(token=config.get('token'))
    logger.info("Checking if bot is okay")
    logger.info(updater.bot.get_me())
    dispatcher = updater.dispatcher
    el.update_prices()
    logger.info("current price: {}".format(el.price))

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(bot, update):
        logger.warning("Received restart command via Telegram")
        update.message.reply_text('Bot is restarting...')
        logger.debug("writing chat ID {0} to {1}".format(update.message.chat_id, master_file))
        with open(master_file, 'w') as f:
            f.write(str(update.message.chat_id))
        logger.debug("Restarting the thread")
        Thread(target=stop_and_restart).start()

    # Linux only
    def update(bot, update):
        logger.warning("Received Update command via Telegram")
        path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.abspath(os.path.join(path, "..", "update.sh"))
        if os.path.exists(full_path):
            logger.debug("sending notification message")
            update.message.reply_text('Triggering bot update process... See you later!')
            logger.debug("writing chat ID {0} to {1}".format(update.message.chat_id, master_file))
            with open(master_file, 'w') as f:
                f.write(str(update.message.chat_id))
            logger.debug("Stopping Bitfinex WebSocket client")
            logger.debug("Executing the script")
            os.system("nohup " + full_path + " &")
        else:
            logger.error("Update script was not found!")
            update.message.reply_text("Sorry haven't found and update script. Please do the update manually.")

    # dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(CommandHandler('restart', restart, filters=Filters.user(username='@streamtv85')))
    dispatcher.add_handler(CommandHandler('update', update, filters=Filters.user(username='@streamtv85')))

    add_command_handlers(dispatcher)
    add_message_handlers(dispatcher)
    logger.debug("List of registered handlers:")
    for current in list(dispatcher.handlers.values())[0]:
        logger.debug(str(current.callback.__name__))
    logger.info("The bot has started.")
    updater.start_polling()
    master_file = "/tmp/master.txt"
    if os.path.exists(master_file):
        with open(master_file, 'r') as f:
            text = f.read()
        logger.debug("read chat id from " + master_file + " file: " + text)
        updater.bot.send_message(int(text), "I'm back bitches!")
        os.remove(master_file)
    logger.info("The bot is idle.")
    updater.idle()


if __name__ == "__main__":
    main()
