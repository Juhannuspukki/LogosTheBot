import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, error
from numpy import matrix
from random import randint
import json
import emoji
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class Ruutu:
    def __init__(self, miina, numero, hidden):
        self.miina = miina
        self.numero = numero
        self.hidden = hidden


def printtaa(lauta, n):
    x = ""
    for i in range(n):
        for a in range(n):
            if lauta.item((i, a)).miina is False:
                x += "|" + str(lauta.item((i, a)).numero)
            else:
                x += "|P"

        x += "|\n"
    print(x)


def settings(bot, update, args):
    ad = update.message.chat_id
    try:
        n = int(args[0])
        miinoja = int(args[1])
        maxmines = int(n * 3)

        if n < 4:
            n = 4
        if n > 10:
            n = 10

        if miinoja < 1:
            miinoja = 1
        if miinoja > maxmines:
            miinoja = maxmines

        with open('beersweepersettings.json', 'r') as fp:
            diktaattori = json.load(fp)

        diktaattori[str(ad)] = n, miinoja

        with open('beersweepersettings.json', 'w') as file:
            json.dump(diktaattori, file, sort_keys=False, indent=4, separators=(',', ': '))

        update.message.reply_text("Success.")

    except (ValueError, IndexError) as err:
        update.message.reply_text("Usage: /beersweepersettings <gridheight> <mines>\n"
                                  "For example /beersweepersettings 10 16 to set height to 10 and mines to 16")


def generatedefault(n):
    lista = []
    toinenlista = []
    for i in range(n):
        for a in range(8):
            toinenlista.append(Ruutu(False, 0, True))
        lista.append(toinenlista)
        toinenlista = []
    lauta = matrix(lista)
    return lauta


def generatehelper(lauta, x, y, n):
    if x < 0 or y < 0 or x > n - 1 or y > 7:
        return lauta
    else:
        lauta.item((x, y)).numero += 1
    return lauta


def generatekeyboard(lauta, n):
    lista = []
    toinenlista = []
    for i in range(n):
        for a in range(8):
            if lauta.item((i, a)).hidden is False:
                if lauta.item((i, a)).numero == 0:
                    toinenlista.append(InlineKeyboardButton(" ", callback_data=("ö" + str(i) + str(a))))
                else:
                    toinenlista.append(
                        InlineKeyboardButton(str(lauta.item((i, a)).numero), callback_data=("ö" + str(i) + str(a))))
            else:
                toinenlista.append(InlineKeyboardButton(emoji.emojize(":beer_mug:"), callback_data=("ö" + str(i) + str(a))))

        lista.append(toinenlista)
        toinenlista = []
    return lista


def generate(n, miinoja, x, y):
    while True:
        lauta = generatedefault(n)
        w = 0
        while w < miinoja:
            int1 = randint(0, n - 1)
            int2 = randint(0, 7)
            if lauta.item((int1, int2)).miina is False:
                lauta.item((int1, int2)).miina = True
                w += 1

        for i in range(n):
            for a in range(8):
                if lauta.item((i, a)).miina is True:
                    lauta = generatehelper(lauta, i, a + 1, n)
                    lauta = generatehelper(lauta, i, a - 1, n)
                    lauta = generatehelper(lauta, i + 1, a, n)
                    lauta = generatehelper(lauta, i - 1, a, n)
                    lauta = generatehelper(lauta, i - 1, a - 1, n)
                    lauta = generatehelper(lauta, i + 1, a - 1, n)
                    lauta = generatehelper(lauta, i - 1, a + 1, n)
                    lauta = generatehelper(lauta, i + 1, a + 1, n)

        if lauta.item((x, y)).numero == 0:
            break

    return lauta


def revealhelper(lauta, x, y, gonethrough, n):
    if x < 0 or y < 0 or x > n - 1 or y > 7:
        return lauta
    else:
        lauta.item((x, y)).hidden = False

    if lauta.item((x, y)).numero == 0 and (x, y) not in gonethrough:
        return testi(x, y, gonethrough, lauta, n)

    return lauta


def testi(x, y, gonethrough, lauta, n):
    if lauta.item((x, y)).numero == 0:
        gonethrough.append((x, y))
        lauta = revealhelper(lauta, x, y + 1, gonethrough, n)
        lauta = revealhelper(lauta, x, y - 1, gonethrough, n)
        lauta = revealhelper(lauta, x + 1, y, gonethrough, n)
        lauta = revealhelper(lauta, x - 1, y, gonethrough, n)
        lauta = revealhelper(lauta, x - 1, y - 1, gonethrough, n)
        lauta = revealhelper(lauta, x + 1, y - 1, gonethrough, n)
        lauta = revealhelper(lauta, x - 1, y + 1, gonethrough, n)
        lauta = revealhelper(lauta, x + 1, y + 1, gonethrough, n)
    return lauta


def reveal(x, y, lauta, n):
    gonethrough = []
    if lauta.item((x, y)).miina is False:
        lauta.item((x, y)).hidden = False
        if lauta.item((x, y)).numero == 0:
            lauta = testi(x, y, gonethrough, lauta, n)
            return lauta
        else:
            return lauta
    else:
        return lauta


def checkwin(lauta, n, miinoja):
    try:
        win = 0
        for i in range(n):
            for a in range(8):
                if lauta.item((i, a)).hidden is False:
                    win += 1

        if win >= 8 * n - miinoja:
            return True
        else:
            return False
    except AttributeError:
        return False


def startgame(bot, update):
    ad = update.message.chat_id
    with open('beersweepersettings.json', 'r') as fp:
        despootti = json.load(fp)

    try:
        n = despootti[str(ad)][0]
        miinoja = despootti[str(ad)][1]
    except KeyError:
        n = 8
        miinoja = 8

    lauta = generatedefault(n)
    keyboard = generatekeyboard(lauta, n)
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open('miinaharava.json', 'r') as fp:
        diktaattori = json.load(fp)

    diktaattori[str(update.message.chat_id)] = [n, miinoja, 0, saving(lauta, n)]

    with open('miinaharava.json', 'w') as file:
        json.dump(diktaattori, file, sort_keys=False, indent=4, separators=(',', ': '))

    bot.sendMessage(chat_id=ad, text="Choose:", reply_markup=reply_markup)


def game(bot, update, lauta, n, ad=0, md=0):
    keyboard = generatekeyboard(lauta, n)
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        bot.editMessageText(chat_id=ad, message_id=md, text="Choose:", reply_markup=reply_markup)
    except error.TelegramError:
        pass


def saving(lauta, n):
    lista = []
    toinenlista = []
    for i in range(n):
        for a in range(8):
            toinenlista.append(
                [bool(lauta.item((i, a)).miina), int(lauta.item((i, a)).numero), bool(lauta.item((i, a)).hidden)])
        lista.append(toinenlista)
        toinenlista = []

    return lista


def button(bot, update):
    query = update.callback_query
    with open('miinaharava.json', 'r') as fp:
        diktaattori = json.load(fp)
    lauta = diktaattori[str(query.message.chat_id)][3]
    n = diktaattori[str(query.message.chat_id)][0]
    starttime = diktaattori[str(query.message.chat_id)][2]
    miinoja = diktaattori[str(query.message.chat_id)][1]
    for i in range(n):
        for a in range(8):
            lauta[i][a] = Ruutu(bool(lauta[i][a][0]), int(lauta[i][a][1]), bool(lauta[i][a][2]))

    lauta = matrix(lauta)

    p = 0

    x = int(query.data[1])
    y = int(query.data[2])

    for i in range(n):
        for a in range(8):
            if lauta.item((i, a)).hidden is False:
                p = 1
                break

    if p == 0:
        while True:
            lauta = generate(n, miinoja, x, y)
            lauta = reveal(x, y, lauta, n)
            starttime = str(datetime.datetime.now())
            if checkwin(lauta, n, miinoja) is False:
                break

    else:
        if lauta.item((x, y)).miina is False:
            lauta = reveal(x, y, lauta, n)

        else:
            bot.editMessageText(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                text="Sorry, this beer is poisoned!")
            return

        if checkwin(lauta, n, miinoja) is True:
            now = datetime.datetime.now()
            delta = now - datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f")
            combined = delta.seconds + delta.microseconds / 1E6
            bot.editMessageText(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                text=("You won! Your time: {:.2f}".format(combined)))
            return

    diktaattori[str(query.message.chat_id)] = [n, miinoja, starttime, saving(lauta, n)]

    with open('miinaharava.json', 'w') as file:
        json.dump(diktaattori, file, sort_keys=False, indent=4, separators=(',', ': '))

    return game(bot, update, lauta, n, query.message.chat_id, query.message.message_id)
