import logosshorties
from numpy.random import choice
import random

import json


badkeywords = ["paska", "perhana", "pers", "vittu", " vitu", "jumalaut", "fuck", "shit", "hitto", "helvet", "perkele",
               "prkl", "saatana", "stna", "saamari"]


muuttuja = False


def location(bot, update):
    user_location = update.message.location
    if 61.460883 > user_location.latitude > 61.435294 and 23.884317 > user_location.longitude > 23.824617:
        update.message.reply_text("Herwannassa!")
    elif 61.515019 > user_location.latitude > 61.458427 and 23.872946 > user_location.longitude > 23.661869:
        update.message.reply_text("Mansessa.")
    elif 60.462486 > user_location.latitude > 60.436182 and 22.322561 > user_location.longitude > 22.219996:
        update.message.reply_text("Turussa.")
    elif 61.145544 > user_location.latitude > 61.106880 and 21.558158 > user_location.longitude > 21.422560:
        update.message.reply_text("Raumalla.")
    else:
        update.message.reply_text("Korvessa.")


def echo(bot, update):
    # init
    # syntax 1: one in list, 2: random choice, 3: weighted random
    viesti = update.message.text.lower()
    chat_id = str(update.message.chat_id)

    with open('saves.json', 'r') as fp:
        swearjardict = json.load(fp)
    with open('wordlists.json', 'r') as fp:
        wordlists = json.load(fp)

    if chat_id not in swearjardict:
        swearjardict[str(chat_id)] = {}

    thischat = swearjardict[chat_id]
    thisguy = logosshorties.usrname(bot, update)
    if thisguy not in thischat.keys() and thisguy != "@":
        thischat[thisguy] = 0

    # finding stuff
    global muuttuja
    if (viesti.find("paska botti") != -1 or viesti.find("tyhmä botti") != -1) and muuttuja is False:
        update.message.reply_text(u"\U0001F595")
        muuttuja = True
        return

    for items in badkeywords:
        if viesti.find(items) != -1:
            if thisguy in thischat.keys():
                thischat[thisguy] += 1
                with open('saves.json', 'w') as file:
                    json.dump(swearjardict, file, sort_keys=True, indent=4, separators=(',', ': '))

    for keys in wordlists.keys():
        if viesti.find(keys) != -1:
            keydata = wordlists[keys]
            pasila = keydata[1]
            listlen = pasila[0]
            tyyppi = pasila[1]
            randomtype = pasila[2]
            if randomtype == "1":
                printable = keydata[0][0]
                logosshorties.sendhelper(bot, update, int(chat_id), printable, tyyppi)
                break

            elif randomtype == "2":
                printable = random.choice(keydata[0])
                logosshorties.sendhelper(bot, update, int(chat_id), printable, tyyppi)
                break

            elif randomtype == "3":
                probability = []
                for i in range(listlen):
                    probability.append(0.1/listlen)
                probability.append(0.9)
                printable = choice(keydata[0], p=probability)
                logosshorties.sendhelper(bot, update, int(chat_id), printable, tyyppi)
                break


def swearjar(bot, update):
    x = ""
    chatid = str(update.message.chat_id)
    with open('saves.json', 'r') as fp:
        swearjardict = json.load(fp)

    try:
        thischat = swearjardict[chatid]
        if chatid in swearjardict.keys():
            for nimet in sorted(thischat.keys()):
                if thischat[nimet] == 0:
                    pass
                else:
                    x = x + nimet + ": " + str(thischat[nimet]) + "\n"
            update.message.reply_text(x)
    except KeyError:
        update.message.reply_text("I haven't recorded any uses of bad language in this chat yet.")

