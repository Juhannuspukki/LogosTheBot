import random
import json
import datetime


def help(bot, update):
    update.message.reply_text("Logos Mk XIV, at your service! Usage:"
                              "\n\n/liiga - SM-liigan sarjataulukko"
                              "\n/menu - TTY:n päivän ruokalistat"
                              "\n/open - check if a service is available right now at the campus"
                              "\n/xkcd - gives you a random xkcd comic to read"
                              "\n/hype - 11/28/16"
                              "\n/laulu - lyrics for a random teekkari song"
                              "\n/swearjar - view the contents of the swear jar"
                              "\n/skål - logs a drink that contains 12g, 26g, 32g or 0g of alcohol to the system"
                              "\n/promillet - how drunk you are at the moment... at least in theory"
                              "\n/accounthelp - information concerning accounts"
                              "\n/log - show the update log"
                              "\n/latin <search> - Search a finnish phrase in the latin dictionary"
                              "\n/cam - Herwantacam"
                              "\n/telok <search> - Search for items in the TELOK database"
                              "\n/nysse <line> - Find the location of a nysse near you"
                              "\n/moveme <a/d> <hour> <minute> - Going places. Optional args for arrival/departure and "
                              "time. For example /moveme a 16 00 if you want to be somewhere at 16:00 o'clock."
                              "\n/beersweeper - Play a game of beersweeper. It's almost like minesweeper, but not quite"
                              "\n/beersweepersettings - Adjust the settings of your beersweeper board"
                              "\n\n/set <x> - set the timer to x seconds. Default: 7 minutes"
                              "\n/unset - cancel the timer"
                              "\n\n/kääretorttu")


def accounthelp(bot, update):
    update.message.reply_text("An account is based on your username and chat id. Accounts are required to use"
                              "/promillet for example."
                              "\n/createaccount <weight> <gender(M/F)>"
                              "\n/deleteaccount - deletes your account and all your data"
                              "\n/accounthelp - information concerning accounts"
                              "\nSo, if you are a 80kg guy then best results are achieved with /createaccount 80 M "
                              "for example")


def latin(bot, update, args):

    with open('latinf.json', 'r') as fp:
        latina = json.load(fp)

    if args:
        f = False
        arg = ""
        lista = ""

        for i in range(len(args)):
            arg = arg + " " + args[i]

        arg = arg[1:]
        arg = arg.lower()

        for keys in latina.keys():
            avain = keys.lower()
            if avain.find(arg) != -1:
                lista = lista + keys + " - " + latina[keys] + "\n"
                f = True

        if f is False:
            update.message.reply_text("Nothing found.")
            return
        update.message.reply_text(lista)

    else:
        thischat = update.message.chat_id
        thisuser = update.message.from_user.id
        if thischat == thisuser:
            lista = ""
            for keys in sorted(latina.keys()):
                lista = lista + keys + " - " + latina[keys] + "\n"
                if len(lista) > 3900:
                    update.message.reply_text(lista)
                    lista = ""
            update.message.reply_text(lista)
        else:
            pass


def laulu(bot, update):
    x = []
    with open("Logos.txt", encoding="utf-8") as fp:
        for line in fp:
            x.append(line)

    kokotiedosto = "".join(x)
    songs = kokotiedosto.split("///")

    update.message.reply_text(random.choice(songs))


def log(bot, update):
    update.message.reply_text("Update 10/10/16: fixed account creation, fixed /xkcd (twice), added log, new keywords, "
                              "replacing text with numbers, local file handling\n\nUpdate 11/10/16: fixed xkcd(again) "
                              "added /latin for a small latin pocketref. Other bug fixes. Dictum, factum.\n\nUpdate "
                              "18/12/16: /cam functionality enabled. Small tweaks to system.\n\nUpdate "
                              "21/12/16: added /telok. Added /open.\n\nUpdate 12/1/17: total overhaul to /menu, fixed "
                              "a typo in /telok\n\nUpdate 23/1/17: /open actually does stuff and things now. Camera "
                              "hw changes.\n\nUpdate 2/2/2017: added /nysse, fixed an issue with /telok.\n\nUpdate 3/2"
                              "/2017: fixed an issue with /nysse.\n\nUpdate 25/2/2017: added /beersweeper, "
                              "added /beersweepersettings.\n\nUpdate 12/3/2017: added /moveme.")


def avoinna(bot, update):

    x = ""
    times = {"alkuviikko": {"Newton": ["10:30:00", "16:00:00"], "SÅÅSBAR": ["10:30:00", "19:00:00"],
                            "Fusari": ["10:30:00", "8:45:00"], "Reaktori": ["10:30:00", "15:00:00"],
                            "Supper at Reaktori": ["16:00:00", "18:00:00"], "Hertsi": ["10:30:00", "15:00:00"],
                            "M Room": ["8:00:00", "16:00:00"], "M Room student discount": ["10:00:00", "14:00:00"]},

             "perjantai": {"Newton": ["10:30:00", "15:00:00"], "SÅÅSBAR": ["10:30:00", "19:00:00"],
                           "Fusari": ["10:30:00", "18:45:00"], "Reaktori": ["10:30:00", "15:00:00"],
                           "Supper at Reaktori": ["ööö", "ööö"], "Hertsi": ["10:30:00", "15:00:00"],
                           "M Room": ["8:00:00", "16:00:00"],
                           "M Room student discount": ["ööö", "ööö"]},

             "lauantai": {"Newton": ["ööö", "ööö"], "SÅÅSBAR": ["ööö", "ööö"],
                          "Fusari": ["ööö", "ööö"], "Reaktori": ["11:00:00", "15:00:00"],
                          "Supper at Reaktori": ["ööö", "ööö"],
                          "Hertsi": ["ööö", "ööö"], "M Room": ["ööö", "ööö"],
                          "M Room student discount": ["ööö", "ööö"]}}

    day = datetime.datetime.now().weekday()
    now = str(datetime.datetime.now().time())[:-7]
    FMT = "%H:%M:%S"
    if day == 5:
        key = "lauantai"
    elif day == 4:
        key = "perjantai"
    else:
        key = "alkuviikko"

    primetime = times[key]
    for key in sorted(primetime):
        openingtime = primetime[key][0]
        if openingtime != "ööö":
            closingtime = primetime[key][1]
            timeuntilclose = datetime.datetime.strptime(closingtime, FMT) - datetime.datetime.strptime(now, FMT)
            timeuntilopen = datetime.datetime.strptime(openingtime, FMT) - datetime.datetime.strptime(now, FMT)

            if timeuntilclose.days < 0:
                x += key + " is currently closed.\n"
            elif timeuntilopen.days >= 0:
                x += key + " will open in " + str(timeuntilopen) + "\n"
            else:
                x += key + " is open for " + str(timeuntilclose) + "\n"

    update.message.reply_text(x)