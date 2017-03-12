from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import datetime as dt
import googlemaps

SORSA, DESTINATION = range(2)
beginning = None
time = "d", datetime.now()


def start(bot, update, args):
    if args:
        try:
            if args[0] == "a" or args[0] == "d":
                global time
                time = args[0], datetime.combine(datetime.now().date(), dt.time(int(args[1]), int(args[2])))
                bot.sendMessage(chat_id=update.message.chat_id, text="Please send your current location.")
                return SORSA
            else:
                raise TypeError
        except (ValueError, IndexError, TypeError) as error:
            update.message.reply_text("Usage: /moveme <a/d> <hour> <minute>")
            return

    bot.sendMessage(chat_id=update.message.chat_id, text="Please send your current location.")
    return SORSA


def startlocationquery(bot, update):
    global beginning
    beginning = str(update.message.location.latitude) + "," + str(update.message.location.longitude)
    update.message.reply_text("Please send your destination.")

    return DESTINATION


def startlocationtextquery(bot, update):
    global beginning
    beginning = update.message.text
    update.message.reply_text("Please send your destination.")

    return DESTINATION


def endlocationquery(bot, update):
    end = str(update.message.location.latitude) + "," + str(update.message.location.longitude)
    return hitchhikersguidetonysse(bot, update, end)


def endlocationtextquery(bot, update):
    end = update.message.text
    return hitchhikersguidetonysse(bot, update, end)


def hitchhikersguidetonysse(bot, update, end):
    chatid = str(update.message.chat_id)

    gmaps = googlemaps.Client(key='AIzaSyA1VGRpW2jVM0rgb6WIxQlqRIcb5qy_GYM')

    # Request directions via public transit
    try:
        if time[0] == "d":
            directions = gmaps.directions(beginning, end, mode="transit", departure_time=time[1], alternatives=True)
        if time[0] == "a":
            directions = gmaps.directions(beginning, end, mode="transit", arrival_time=time[1], alternatives=True)

    except googlemaps.exceptions.ApiError:
        bot.sendMessage(chat_id=chatid, text="Your search was sadly unfruitful. Try some other location or address.")
        return ConversationHandler.END

    textvar = ""
    biggerbuttonlist = []
    for items in directions:
        endzonecoords = str(items["legs"][0]["steps"][-1]["end_location"]["lat"]) + "," + \
                        str(items["legs"][0]["steps"][-1]["end_location"]["lng"])

        finaldestination = [InlineKeyboardButton("Destination", callback_data=endzonecoords)]

        for z in items["legs"][0]["steps"]:
            textvar += z["html_instructions"] + ", " + z["duration"]["text"] + "\n"
            try:
                transdetdepart = z["transit_details"]["departure_stop"]
                transdetarrive = z["transit_details"]["arrival_stop"]
                textvar += "Line " + z["transit_details"]["line"]["short_name"] + " from "
                textvar += transdetdepart["name"] + " (" + z["transit_details"]["departure_time"]["text"] + ") to "
                textvar += transdetarrive["name"] + " (" + z["transit_details"]["arrival_time"]["text"] + ")\n"

                x = transdetdepart["name"]
                y = transdetarrive["name"]

                departcoords = str(transdetdepart["location"]["lat"]) + "," + str(transdetdepart["location"]["lng"])
                arrivalcoords = str(transdetarrive["location"]["lat"]) + "," + str(transdetarrive["location"]["lng"])
                buttonlist = [InlineKeyboardButton(x, callback_data=departcoords),
                              InlineKeyboardButton(y, callback_data=arrivalcoords)]
                biggerbuttonlist.append(buttonlist)
            except KeyError:
                pass

        biggerbuttonlist.append(finaldestination)
        reply_markup = InlineKeyboardMarkup(biggerbuttonlist)

        bot.sendMessage(chat_id=chatid, text=textvar, reply_markup=reply_markup)

        textvar = ""
        biggerbuttonlist = []

    return ConversationHandler.END


def button(bot, update):
    query = update.callback_query
    ad = str(query.message.chat_id)
    coords = query.data.split(",")
    bot.sendLocation(chat_id=ad, latitude=coords[0], longitude=coords[1])


def cancel(bot, update):
    reply_markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id=update.message.chat_id, text="Operation cancelled.", reply_markup=reply_markup)
    return ConversationHandler.END


tech2 = ConversationHandler(
    entry_points=[CommandHandler('moveme', start, pass_args=True)],

    states={
        SORSA: [MessageHandler(Filters.location, startlocationquery), MessageHandler(Filters.text, startlocationtextquery)],
        DESTINATION: [MessageHandler(Filters.location, endlocationquery), MessageHandler(Filters.text, endlocationtextquery)],

    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
