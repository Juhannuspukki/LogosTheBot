import json
import logosshorties


def createaccount(bot, update, args):

    with open('accounts.json', 'r') as file:
        accounts = json.load(file)

    chatid = str(update.message.chat_id)
    now = str(update.message.date)

    if chatid not in accounts.keys():
        accounts[chatid] = {}
        update.message.reply_text("Chat ID added.")
        with open('accounts.json', 'w') as file:
            json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))

    thischataccount = accounts[chatid]
    errormsg = "Usage: /createaccount <weight> <gender(M/F)>"

    try:
        äää = int(args[0])
    except (IndexError, ValueError):
        update.message.reply_text(errormsg)
        return

    öö = logosshorties.usrname(bot, update)
    if (args[1] == "M" or args[1] == "F") and äää > 0:
        if öö not in thischataccount.keys() and öö != "@":
            thischataccount[öö] = [args[0], args[1], 0, now]
            update.message.reply_text("Account created.")
            with open('accounts.json', 'w') as file:
                json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))
        else:
                update.message.reply_text("Account already exists or you have no username!")
    else:
        update.message.reply_text(errormsg)


def deleteaccount(bot, update):
    with open('accounts.json', 'r') as file:
        accounts = json.load(file)

    chatid = str(update.message.chat_id)
    thischataccount = accounts[chatid]
    öö = logosshorties.usrname(bot, update)
    if chatid in accounts.keys() and öö != "@":
        if öö in thischataccount.keys():
            del thischataccount[öö]
            update.message.reply_text("Account deleted.")
            with open('accounts.json', 'w') as file:
                json.dump(accounts, file, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            update.message.reply_text("No account found.")
    else:
        return
