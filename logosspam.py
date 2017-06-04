from datetime import datetime
from datetime import date
import requests
import json
import logosmenu
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)


NIMIPÄIVÄ, RAVINTOLA, SÄÄ, SIJAINTI, TIME = range(5)


def includer(bot, job):
    with open('spams.json', 'r') as fie:
        accounts = json.load(fie)

    chat_id = job.context

    päiväspämmi = ""
    for i in range(len(accounts)):
        if accounts[i]["chat_id"] == chat_id:
            if accounts[i]["namedays"] == "true":
                päiväspämmi += "Namedays today: " + namedays() + "\n\n"
            if accounts[i]["weather"] == "true":
                päiväspämmi += säätiedot(accounts[i])
            if accounts[i]["restaurant"] == "newton":
                päiväspämmi += logosmenu.juvenes()
            if accounts[i]["restaurant"] == "reaktori":
                päiväspämmi += logosmenu.returnreaktori()
            if accounts[i]["restaurant"] == "hertsi":
                päiväspämmi += logosmenu.returnhertsi()

            bot.sendMessage(job.context, text=päiväspämmi)
            return


def namedays():
    d = date.today()
    key = str(d.day) + "." + str(d.month) + "."
    url = "http://www.iltalehti.fi/json/nimipvm.json"
    x = requests.get(url)
    x = x.content.decode("utf-8")
    feed = json.loads(x)
    lista = feed[key]
    finallist = ", ".join(lista)

    return finallist


def säätiedot(account):
    url = "https://api.darksky.net/forecast/83fcef161687520d6b92fad2136a720c/" + account[
        "coords"] + "?units=si&exclude=minutely"
    x = requests.get(url)
    x = x.content.decode("utf-8")
    feed = json.loads(x)

    sää = "Current weather: "
    sää += feed["currently"]["summary"] + "\n🌡: " + str(feed["currently"]["temperature"]) + "ºC "
    sää += "(" + str(feed["currently"]["apparentTemperature"]) + "ºC)\n"
    sää += "💧: " + str(feed["currently"]["dewPoint"]) + "ºC & "
    sää += str(feed["currently"]["humidity"] * 100)[:2] + "%\n"
    sää += "☁️: " + str(feed["currently"]["cloudCover"] * 100) + "%\n"

    sää += "💨️️: " + str(feed["currently"]["windSpeed"]) + "m/s "
    windbearing = feed["currently"]["windBearing"]
    if windbearing < 22.5 or windbearing > 337.5:
        sää += "⬇️\n "
    elif windbearing < 67.5:
        sää += "↙️️\n "
    elif windbearing < 112.5:
        sää += "⬅️\n "
    elif windbearing < 157.5:
        sää += "↖️\n "
    elif windbearing < 202.5:
        sää += "⬆️\n "
    elif windbearing < 247.5:
        sää += "↗️\n "
    elif windbearing < 292.5:
        sää += "➡️\n "
    elif windbearing < 337.5:
        sää += "↘️\n "

    return sää + "\n\n"


def loadspams(job_queue, chat_data):
    with open('spams.json', 'r') as fie:
        accounts = json.load(fie)

    for i in range(len(accounts)):
        thisuser = accounts[i]
        if thisuser["chat_id"] == "true":
            chat_id = int(thisuser["chat_id"])  # HAS TO BE int, if using string as key shit goes sideways
            fmt = "%H:%M:%S"
            timeis = datetime.strptime(thisuser["time"], fmt).time()
            job = job_queue.run_daily(includer, timeis, context=chat_id, name="dailyspam")
            chat_data[chat_id]["dailyspam"] = job


def spam(bot, update, job_queue, chat_data):
    if "dailyspam" in chat_data:
        update.message.reply_text('Spam already active!')
        return
    else:
        with open('spams.json', 'r') as fie:
            accounts = json.load(fie)

        chat_id = str(update.message.chat_id)

        for i in range(len(accounts)):
            thisuser = accounts[i]
            if thisuser["chat_id"] == chat_id:
                fmt = "%H:%M:%S"
                timeis = datetime.strptime(thisuser["time"], fmt).time()
                job = job_queue.run_daily(includer, timeis, context=chat_id, name="dailyspam")
                chat_data["dailyspam"] = job

                thisuser["enabled"] = "true"
                with open('spams.json', 'w') as file:
                    json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))
                update.message.reply_text('Spam successfully loaded!')
                return

        update.message.reply_text('Spam content information not set! /spamsettings')


def unspam(bot, update, chat_data):
    if "dailyspam" not in chat_data:
        update.message.reply_text('You have no spam to cancel!')

    else:
        job = chat_data["dailyspam"]
        job.schedule_removal()
        del chat_data["dailyspam"]
        update.message.reply_text('Spam successfully unset!')

        chat_id = str(update.message.chat_id)

        with open('spams.json', 'r') as fie:
            accounts = json.load(fie)

        for i in range(len(accounts)):
            thisuser = accounts[i]
            if thisuser["chat_id"] == chat_id:
                thisuser["enabled"] = "false"
                with open('spams.json', 'w') as file:
                    json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))
                return

        update.message.reply_text('You have no active spam!')


def updateinformation(update, parameter, value):
    chat_id = str(update.message.chat_id)

    with open('spams.json', 'r') as flie:
        accounts = json.load(flie)

    for i in range(len(accounts)):
        thisuser = accounts[i]
        if thisuser["chat_id"] == chat_id:
            thisuser[parameter] = value

    with open('spams.json', 'w') as file:
        json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))


def spamsettings(bot, update):
    reply_keyboard = [["✅", "🚫"]]
    chat_id = str(update.message.chat_id)
    check = False

    with open('spams.json', 'r') as flie:
        accounts = json.load(flie)

        for i in range(len(accounts)):
            thisuser = accounts[i]
            if thisuser["chat_id"] == chat_id:
                check = True

        if not check:
            accounts.append(
                {"chat_id": chat_id, "coords": "61.4481,23.8521", "enabled": "false", "namedays": "false",
                 "restaurant": "none", "time": "00:00:00", "weather": "false"})

    with open('spams.json', 'w') as file:
        json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))

    update.message.reply_text(
        "First of all, would you like to receive information about Finnish namedays?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return NIMIPÄIVÄ


def nimipäivä(bot, update):
    response = str(update.message.text)
    if response == "✅":
        updateinformation(update, "namedays", "true")
    else:
        updateinformation(update, "namedays", "false")
    reply_keyboard = [["Newton", "Reaktori"], ["Hertsi", "🚫"]]
    update.message.reply_text(
        "Would you like to receive information restaurant menus at TUT?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RAVINTOLA


def ravintola(bot, update):
    response = str(update.message.text)
    if response == "🚫":
        updateinformation(update, "restaurant", "none")
    else:
        updateinformation(update, "restaurant", response)
    reply_keyboard = [["✅", "🚫"]]
    update.message.reply_text(
        "Would you like to receive information about the weather? (Requires location information)",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SÄÄ


def sää(bot, update):
    response = str(update.message.text)
    if response == "✅":
        updateinformation(update, "weather", "true")
    else:
        updateinformation(update, "weather", "false")
        return TIME
    update.message.reply_text("Please send your location.", reply_markup=ReplyKeyboardRemove())
    return SIJAINTI


def sijainti(bot, update):
    response = update.message.location
    updateinformation(update, "coords", (str(response.latitude) + "," + str(response.longitude)))
    update.message.reply_text(
        "When would you like to receive your daily newsletter? The correct format for this is <hh:mm:ss> with leading "
        "zeros. For example you can type 06:00:00 to receive it at 6 o'clock in the morning.",
        reply_markup=ReplyKeyboardRemove())
    return TIME


def time(bot, update):
    response = str(update.message.text)
    try:
        fmt = "%H:%M:%S"
        timeis = datetime.strptime(response, fmt).time()
        updateinformation(update, "time", str(timeis))
        update.message.reply_text("Success. Use /spam to activate.", reply_markup=ReplyKeyboardRemove())
    except ValueError:
        update.message.reply_text("Incorrect format. Please try again.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text('Operation cancelled.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


createspam = ConversationHandler(
        entry_points=[CommandHandler('spamsettings', spamsettings)],

        states={
            NIMIPÄIVÄ: [RegexHandler("^(✅|🚫)$", nimipäivä)],
            RAVINTOLA: [RegexHandler("^(Newton|Reaktori|Hertsi|🚫)$", ravintola)],
            SÄÄ: [RegexHandler("^(✅|🚫)$", sää)],
            SIJAINTI: [MessageHandler(Filters.location, sijainti)],
            TIME: [MessageHandler(Filters.text, time)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )