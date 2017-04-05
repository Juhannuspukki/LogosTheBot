from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import error


identification = ""
RELAYID, RELAYMESSAGE = range(2)


def relaystart(bot, update):
    update.message.reply_text("Chat ID?")
    return RELAYID


def relaytransfer(bot, update):
    global identification
    identification = str(update.message.text)
    update.message.reply_text("Text to send:")
    return RELAYMESSAGE


def relay(bot, update):
    ftl = "You have a new relayed message. The message is as follows: \n\n"
    ftl += str(update.message.text)
    ftl += "\n\nEnd of message."

    try:
        bot.sendMessage(chat_id=identification, text=ftl)
        update.message.reply_text("Message sent.")

    except error.TelegramError:
        update.message.reply_text("Operation failed.")

    return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

relayswitch = ConversationHandler(

    entry_points=[CommandHandler('relay', relaystart)],

    states={

        RELAYID: [MessageHandler(Filters.text, relaytransfer), CommandHandler('cancel', cancel)],
        RELAYMESSAGE: [MessageHandler(Filters.text, relay), CommandHandler('cancel', cancel)],

    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

