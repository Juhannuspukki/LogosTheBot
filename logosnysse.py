from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
import json
import requests


SUUNTA, LOCATION = range(2)
nysselista = []
essence = ""


def nysse(bot, update, args):
    global essence
    tempref = []
    try:
        essence = args[0]
    except IndexError:
        update.message.reply_text("Usage: /nysse <line number>")
        return ConversationHandler.END

    informaatio = nysselokaattori()
    for i in range(len(informaatio)):
        a = informaatio[i]
        b = a["MonitoredVehicleJourney"]
        line = b["LineRef"]["value"]
        if line == essence:
            destination = b["DestinationName"]["value"]
            if destination not in tempref:
                tempref.append(destination)
    if tempref:
        reply_keyboard = [tempref]
        update.message.reply_text('Select destination. Send /cancel to cancel.\n\n',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SUUNTA

    else:
        update.message.reply_text("Nysse not found.")
        return ConversationHandler.END


def suunta(bot, update):
    global nysselista
    päämäärä = update.message.text
    informaatio = nysselokaattori()
    for i in range(len(informaatio)):
        a = informaatio[i]
        b = a["MonitoredVehicleJourney"]
        destination = b["DestinationName"]["value"]
        line = b["LineRef"]["value"]
        if destination == päämäärä and line == essence:
            latitude = b["VehicleLocation"]["Latitude"]
            longitude = b["VehicleLocation"]["Longitude"]
            nysselista.append((latitude, longitude))

    update.message.reply_text('Please send your location. Send /cancel to cancel.\n\n')
    return LOCATION


def sijainti(bot, update):
    global nysselista
    diktaattori = {}
    reply_markup = ReplyKeyboardHide()
    bot.sendMessage(chat_id=update.message.chat_id, text="Success.", reply_markup=reply_markup)
    user_location = update.message.location
    for i in range(len(nysselista)):
        latdelta = abs(nysselista[i][0] - user_location.latitude)
        longdelta = abs(nysselista[i][1] - user_location.longitude)
        totaldelta = latdelta + longdelta
        diktaattori[totaldelta] = nysselista[i][0], nysselista[i][1]
    x = min(diktaattori, key=diktaattori.get)
    update.message.reply_location(diktaattori[x][0], diktaattori[x][1])
    nysselista = list()
    return ConversationHandler.END


def nysselokaattori():
    url = "http://data.itsfactory.fi/siriaccess/vm/json"
    x = requests.get(url)
    x = str(x.content)

    x = x[2:-1]
    x = x.replace("\\", "")
    x = x.replace("xc3xb6", "ö")
    x = x.replace("xc3xa4", "ä")

    lokaatio = json.loads(x, encoding='utf-8')
    informaatio = lokaatio["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"]
    return informaatio


def cancel(bot, update):
    reply_markup = ReplyKeyboardHide()
    bot.sendMessage(chat_id=update.message.chat_id, text="Operation cancelled.", reply_markup=reply_markup)
    return ConversationHandler.END


nysset = ConversationHandler(
        entry_points=[CommandHandler('nysse', nysse, pass_args=True)],

        states={
            SUUNTA: [MessageHandler(Filters.text, suunta)],
            LOCATION: [MessageHandler(Filters.location, sijainti)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )