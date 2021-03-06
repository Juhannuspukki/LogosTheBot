from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, RegexHandler
from telegram import ParseMode
import emoji
import json
import logging
import logosshorties
import logosecho
import logosxkcd
import miinaharava
import logospi
import logostimer
import logosmenu
import logosnysse
import logostelok
import logosdrinks
import logoswayfinding
import logosaccounts
import logostextonly
import logosquestionables
import logosrelay
import logosspam
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# simple commands
def start(bot, update):
    update.message.reply_text("Good day, I'm Logos the Bot. Interactions are listed in /help.")


def source(bot, update):
    update.message.reply_text("https://github.com/Juhannuspukki/LogosTheBot")


def marco(bot, update):
    update.message.reply_text("<i>polo</i>", parse_mode=ParseMode.HTML)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    with open('logosmastercontrol.json', 'r') as fp:
        mastercontrol = json.load(fp)
    updater = Updater(mastercontrol["updater"])
    dp = updater.dispatcher
    spamfile = mastercontrol["filename"]
    logosspam.setfile(spamfile)

    logosspam.loadspams(dp.job_queue, dp.chat_data)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("accounthelp", logostextonly.accounthelp))
    dp.add_handler(CommandHandler("advanced", logostextonly.advanced))
    dp.add_handler(CommandHandler("alho", logosquestionables.alho))
    dp.add_handler(CommandHandler("android", logosshorties.android))
    dp.add_handler(CommandHandler("apple", logosshorties.apple))
    dp.add_handler(CommandHandler('beersweeper', miinaharava.startgame))
    dp.add_handler(CommandHandler('beersweepersettings', miinaharava.settings, pass_args=True))
    dp.add_handler(CommandHandler("cam", logospi.cam))
    dp.add_handler(CommandHandler("createaccount", logosaccounts.createaccount, pass_args=True))
    dp.add_handler(CommandHandler("deleteaccount", logosaccounts.deleteaccount))
    dp.add_handler(CommandHandler("help", logostextonly.help))
    dp.add_handler(CommandHandler("hertsi", logosmenu.hertsi))
    dp.add_handler(CommandHandler("hype", logosquestionables.hype))
    dp.add_handler(CommandHandler("hyvinsanottu", logosquestionables.hyvin))
    dp.add_handler(CommandHandler("id", logosshorties.id))
    dp.add_handler(CommandHandler("kääretorttu", logosshorties.kääretorttu))
    dp.add_handler(CommandHandler("latin", logostextonly.latin, pass_args=True))
    dp.add_handler(CommandHandler("laulu", logostextonly.laulu))
    dp.add_handler(CommandHandler("liiga", logosmenu.liiga))
    dp.add_handler(CommandHandler("loc", logosquestionables.loc))
    dp.add_handler(CommandHandler("log", logostextonly.log))
    dp.add_handler(CommandHandler("marco", marco))
    dp.add_handler(CommandHandler("menu", logosmenu.menu))
    dp.add_handler(CommandHandler("newton", logosmenu.newton))
    dp.add_handler(CommandHandler("num", logosshorties.num, pass_args=True))
    dp.add_handler(CommandHandler("open", logostextonly.avoinna))
    dp.add_handler(CommandHandler("alaoviauki", logospi.alaoviauki))
    dp.add_handler(CommandHandler("promillet", logosdrinks.promillet))
    dp.add_handler(CommandHandler("reaktori", logosmenu.reaktori))
    dp.add_handler(CommandHandler("set", logostimer.set, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("spam", logosspam.spam, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("source", source))
    dp.add_handler(CommandHandler("swearjar", logosecho.swearjar))
    dp.add_handler(CommandHandler("telok", logostelok.telok, pass_args=True))
    dp.add_handler(CommandHandler("thx", logosquestionables.thx))
    dp.add_handler(CommandHandler("unset", logostimer.unset))
    dp.add_handler(CommandHandler("unspam", logosspam.unspam, pass_chat_data=True))
    dp.add_handler(CommandHandler("xkcd", logosxkcd.xkcd, pass_args=True))
    dp.add_handler(CommandHandler("weather", logosspam.test))

    dp.add_handler(CallbackQueryHandler(miinaharava.button, pattern=emoji.emojize('^ö.*$')))
    dp.add_handler(CallbackQueryHandler(logoswayfinding.button))
    dp.add_handler(logosnysse.nysset)
    dp.add_handler(logoswayfinding.tech2)
    dp.add_handler(logosdrinks.conv_handler)
    dp.add_handler(logosrelay.relayswitch)
    dp.add_handler(logosspam.createspam)
    dp.add_handler(MessageHandler(Filters.text, logosecho.echo))
    dp.add_handler(MessageHandler(Filters.location, logosecho.location))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
