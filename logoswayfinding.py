from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from math import radians, cos, sin, asin, sqrt
from datetime import datetime, timedelta
import json
import requests
import operator


SORSA, DESTINATION = range(2)
beginning = 0


class Pysäkki:
    def __init__(self, latitude, longitude, name, short, tariffzone):
        self.lat = latitude
        self.long = longitude
        self.name = name
        self.short = short
        self.tariffzone = tariffzone
        self.kmtoend = 0
        self.kmtostart = 0

    def distancetoend(self, coord):
        self.kmtoend = haversine(self, coord)*sqrt(2)

    def distancetobeginning(self, coord):
        self.kmtostart = haversine(self, coord)*sqrt(2)


class Route:
    def __init__(self, ad, stops):
        self.ad = ad
        self.stops = stops

    def validate(self, entrancestop, exitstop, currenttime):
        check1 = False
        for i in range(len(self.stops)):
            if entrancestop.short == self.stops[i]["stopid"]:
                departtime = self.stops[i]["departtime"]
                try:
                    departtime = datetime.strptime(self.stops[i]["departtime"], "%H:%M:%S").time()
                except ValueError:
                    departtime = "00" + departtime[2:]
                    departtime = datetime.strptime(departtime, "%H:%M:%S").time()
                if (currenttime + timedelta(hours=9)).time() > departtime > currenttime.time():
                    check1 = True
            if exitstop.short == self.stops[i]["stopid"] and check1 is True:
                return self

    def departuretime(self, stop):
        for i in range(len(self.stops)):
            if stop.short == self.stops[i]["stopid"]:
                return self.stops[i]["departtime"]


def haversine(ett, två):
    lon1, lat1, lon2, lat2 = map(radians, [ett.long, ett.lat, två.longitude, två.latitude])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6367 * c


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Please send your current location.")

    return SORSA


def locationquery(bot, update):
    global beginning
    beginning = update.message.location
    update.message.reply_text("Please send your destination.")

    return DESTINATION


def hitchhikersguidetonysse(bot, update):
    pysäkit = []

    end = update.message.location

    url = "http://data.itsfactory.fi/journeys/api/1/stop-points"
    x = requests.get(url)
    x = x.content.decode("utf-8")
    simplex = json.loads(x, encoding='utf-8')

    for i in range(len((simplex["body"]))):
        thisstop = simplex["body"][i]
        location = thisstop["location"].split(",")
        stopobject = Pysäkki(float(location[0]), float(location[1]), thisstop["name"],
                             thisstop["shortName"], thisstop["tariffZone"])
        stopobject.distancetobeginning(beginning)
        stopobject.distancetoend(end)
        pysäkit.append(stopobject)

    cmpfun = operator.attrgetter("kmtostart")
    pysäkit.sort(key=cmpfun)

    starttialähimmät = pysäkit[:9]

    cmpfun = operator.attrgetter("kmtoend")
    pysäkit.sort(key=cmpfun)

    endiälähimmät = pysäkit[:9]

    listofroutes = loadroutes()

    validroutes = []
    validstops = []

    for i in range(len(endiälähimmät)):
        print(endiälähimmät[i].short, ", ", sep="", end="")
    for i in range(len(endiälähimmät)):
        print(starttialähimmät[i].short, ", ", sep="", end="")

    now = datetime.now()

    for i in range(len(listofroutes)):
        for startx in range(len(starttialähimmät)):
            for endx in range(len(endiälähimmät)):
                essence = listofroutes[i].validate(starttialähimmät[startx], endiälähimmät[endx], now)
                if essence:
                    if essence not in validroutes:
                        validroutes.append(essence.departuretime(starttialähimmät[startx]))
                        validstops.append(starttialähimmät[startx])

    print(validroutes)
    printvar = ""
    for i in range(len(validstops)):
        printvar += validstops[i].name + ", " + str(validstops[i].kmtostart) + "\n"

    update.message.reply_text(printvar)

    return ConversationHandler.END


def loadroutes():
    with open("exec.json", "r") as fp:
        one = json.load(fp)

    two = []

    for key in one.keys():
        two.append(Route(key, one[key]))

    return two


def validateexceptions():
    with open("nyssemaisteri.json", "r") as fp:
        nyssemaisteri = json.load(fp)
    return nyssemaisteri


def cancel(bot, update):
    reply_markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat_id, text="Operation cancelled.", reply_markup=reply_markup)
    return ConversationHandler.END


tech2 = ConversationHandler(
        entry_points=[CommandHandler('nysse', start)],

        states={
            SORSA: [MessageHandler(Filters.location, locationquery)],
            DESTINATION: [MessageHandler(Filters.location, hitchhikersguidetonysse)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
