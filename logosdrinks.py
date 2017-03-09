from telegram.ext import CommandHandler, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import json
import emoji
import time
import logosshorties
import datetime


name = ""
DRINK = range(1)


def viinatulkki(bot, update):
    global name
    if logosshorties.usrname(bot, update) == name:
        essence = update.message.text
        interpreter = {emoji.emojize(":beer_mug:"): 12, emoji.emojize(":wine_glass:"): 24,
                       emoji.emojize(":cocktail_glass:"): 32, emoji.emojize(":no_entry_sign:"): 0}
        alko = interpreter[essence]

        with open('accounts.json', 'r') as flie:
            accounts = json.load(flie)

        now = str(update.message.date)
        name = logosshorties.usrname(bot, update)
        chatid = str(update.message.chat_id)
        time = update.message.date
        thischataccount = accounts[str(chatid)]
        promillet = float(thischataccount[name][2])

        if name in thischataccount.keys():

            promillet += alko

            thischataccount[name][3] = str(time)
            thischataccount[name][2] = promillet

            promillelaskuri(bot, update, [chatid, name, now])

            with open('accounts.json', 'w') as file:
                json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))

            reply_markup = ReplyKeyboardRemove()
            bot.sendMessage(chat_id=chatid, text="Logged. Cheers!", reply_markup=reply_markup)
            return ConversationHandler.END
        else:
            reply_markup = ReplyKeyboardRemove()
            bot.sendMessage(chat_id=chatid, text="Invalid username.", reply_markup=reply_markup)
            return ConversationHandler.END


def skål(bot, update):
    chatid = str(update.message.chat_id)
    global name
    name = logosshorties.usrname(bot, update)
    with open('accounts.json', 'r') as fie:
        accounts = json.load(fie)

    try:
        if name in accounts[chatid]:
            keyboard = [[emoji.emojize(":beer_mug:"), emoji.emojize(":wine_glass:")],
                        [emoji.emojize(":cocktail_glass:"), emoji.emojize(":no_entry_sign:")]]

            reply_markup = ReplyKeyboardMarkup(keyboard)
            bot.sendMessage(chat_id=chatid, text="Choose well.", reply_markup=reply_markup, one_time_keyboard=True)
            return DRINK

        else:
            reply_markup = ReplyKeyboardRemove()
            bot.sendMessage(chat_id=chatid, text="Invalid username/account not found.", reply_markup=reply_markup)
            return ConversationHandler.END
    except KeyError:
        update.message.reply_text("Account not found.")


def promillet(bot, update):
    x = ""
    with open('accounts.json', 'r') as fie:
        accounts = json.load(fie)
    now = str(update.message.date)
    chatid = str(update.message.chat_id)
    if chatid in accounts.keys():
        for nimet in sorted(accounts[chatid].keys()):
            promi = promillelaskuri(bot, update, [chatid, nimet, now])
            x = x + nimet + ": {:.2f}\n".format(promi)
        update.message.reply_text(x)
    else:
        update.message.reply_text('Chat not found!')


def promillelaskuri(bot, update, args):
    with open('accounts.json', 'r') as fie:
        accounts = json.load(fie)

    username = args[1]
    chatid = args[0]
    thisaccount = accounts[chatid]
    now = datetime.datetime.strptime(args[2], "%Y-%m-%d %H:%M:%S")
    then = datetime.datetime.strptime(thisaccount[username][3], "%Y-%m-%d %H:%M:%S")
    weight = int(thisaccount[username][0])
    sex = thisaccount[username][1]
    thisdrunk = thisaccount[username][2]

    now2 = time.mktime(now.timetuple())
    then = time.mktime(then.timetuple())
    deltainmins = int((now2 - then) / 60)

    newalkoinbody = thisdrunk - weight * 0.1 * deltainmins/60
    if newalkoinbody < 0:
        newalkoinbody = 0

    if sex == "M":
        kännisä = newalkoinbody / (0.75*weight)
    else:
        kännisä = newalkoinbody / (0.66*weight)

    thisaccount[username][2] = newalkoinbody
    thisaccount[username][3] = str(now)
    with open('accounts.json', 'w') as file:
        json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))

    return kännisä


def cancel(bot, update):
    reply_markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat_id, text="Operation cancelled.", reply_markup=reply_markup)
    return ConversationHandler.END


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('skål', skål)],

        states={
            DRINK: [RegexHandler(emoji.emojize('^(:beer_mug:|:wine_glass:|:cocktail_glass:|:no_entry_sign:)$'),
                                 viinatulkki)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
