import logosshorties
import requests
import random
import re
from lxml import html


def xkcd(bot, update, args):
    chatid = update.message.chat_id
    if args:
        arg = ""
        for i in range(len(args)):
            arg = arg + "_" + args[i]
        arg = arg[1:]
        webp = "http://imgs.xkcd.com/comics/" + arg + ".png"

        page = requests.get(webp)
        tree = html.fromstring(page.content)
        check = tree.xpath('//title/text()')
        if check:
            update.message.reply_text("No xkcd found.")
        else:
            photo = webp
            logosshorties.sendphotohelper(bot, update, chatid, photo)

    else:
        while True:
            rng = random.randint(1, 1743)
            webp = "https://xkcd.com/" + str(rng) + "/"
            page = requests.get(webp)
            tree = html.fromstring(page.content)
            check = tree.xpath('//title/text()')
            comic = re.sub("xkcd: ", "", str(check))
            comic = re.sub(" ", "_", str(comic))
            comic = comic[2:]
            comic = comic[:(len(comic)-2)]
            comic = comic.lower()

            webp = "http://imgs.xkcd.com/comics/" + comic + ".png"
            page = requests.get(webp)
            tree = html.fromstring(page.content)
            check = tree.xpath('//title/text()')
            if not check:
                logosshorties.sendphotohelper(bot, update, chatid, webp)
                break
