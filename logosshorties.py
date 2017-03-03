import emoji
import re


def id(bot, update):
    chatid = update.message.chat_id
    update.message.reply_text(chatid)


def sendphotohelper(bot, update, chat_id, photo):
    if photo != "":
        if photo.find("http") == -1:
            bot.sendChatAction(chat_id, 'upload_photo')
            bot.sendPhoto(chat_id=chat_id,
                          photo=open(photo, 'rb'))

        else:
            bot.sendChatAction(chat_id, 'upload_photo')
            update.message.reply_photo(photo)


def sendhelper(bot, update, chatid, printable, tyyppi):
    if printable != "":
        if tyyppi == "photo":
            sendphotohelper(bot, update, int(chatid), printable)
        else:
            update.message.reply_text(printable)


def usrname(bot, update):
    usrnme = update.message.from_user.username
    usrnme = "@", usrnme
    usrnme = "".join(usrnme)
    return usrnme


def apple(bot, update):
    update.message.reply_text(emoji.emojize(":gem_stone:"))


def android(bot, update):
    update.message.reply_text(emoji.emojize(":pile_of_poo:"))


def kääretorttu(bot, update):
    chatid = update.message.chat_id
    bot.sendVideo(chat_id=chatid, video=open("RickAstley-NeverGonnaGiveYouUp.mp4", 'rb'))


def num(bot, update, args):
    x = ""
    for i in range(len(args)):
        word = args[i]
        word = re.sub("o", "0", word)
        word = re.sub("i", "1", word)
        word = re.sub("e", "3", word)
        word = re.sub("a", "4", word)
        word = re.sub("s", "5", word)
        word = re.sub("t", "7", word)
        x = x + " " + word

    update.message.reply_text(x)
