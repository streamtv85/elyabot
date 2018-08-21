from time import sleep

import emoji
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
    logger.debug("effective_message: {}".format(update.effective_message))
    new_members = update.effective_message['new_chat_members']
    new_members_text = ", ".join([item.first_name for item in new_members])
    if new_members_text:
        new_members_text += ", "
    logger.debug("new members: {}".format(new_members_text))
    event_info("Welcoming new member(s)", update, new_members_text)
    # logger.debug("effective_user: {}".format(update.effective_user))
    sleep(3)
    message = """{}Welcome to ELYA community!
Please kindly read the pinned message above for more info on the coin.
If you have any questions, don't hesitate to ask! All the members of the community are happy to answer every question.
If you want to become a distributor of ELYA sim and ELYA pay worldwide please PM @elyacoin""".format(new_members_text)
    bot.send_message(chat_id=update.message.chat_id, text=message)


def debug_info(bot, update):
    logger.debug(' > received message from chat id: ' + str(update.message.chat_id))
    logger.debug(' > from user: ' + str(update.message.from_user))
    logger.debug(' > message text: ' + str(update.message.text))
    # logger.debug(
    #     ' > chat member info: ' + str(bot.get_chat_member(update.message.chat_id, update.message.from_user.id)))


def event_info(prefix, update, message):
    if message:
        suffix = "Response:\n"
    else:
        suffix = ""

    if update.message.from_user.username:
        from_user = update.message.from_user.username
    else:
        from_user = update.message.from_user.first_name
    logger.info(
        prefix + ": chat id {0!s}, user {1!s} ({2}). ".format(
            update.message.chat_id, from_user,
            update.message.from_user.id) + suffix + message)
