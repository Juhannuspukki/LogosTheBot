import mysql.connector
import json


def telok(bot, update, args):
    with open('logosmastercontrol.json', 'r') as fp:
        mastercontrol = json.load(fp)

    keys1 = {}
    keys2 = {}
    lista = ""
    cnx = mysql.connector.connect(user='castor', password=mastercontrol["telokpassword"],
                                  host=mastercontrol["telokaddress"], database='telok')
    cursor = cnx.cursor()
    query = "SELECT * FROM `000`"
    cursor.execute(query)

    for data in cursor:
        keys1[data[0]] = data[1]
        keys2[data[1]] = data[0]

    try:
        haku = args[0]
        haku = haku.title()

        if haku in keys2.keys():
            sök = keys2[haku]
        else:
            sök = "öööö"

        query = "SELECT * FROM komponentit WHERE type LIKE '%{}%' OR name LIKE '%{}%' OR description LIKE '%{}%'".format(
            sök, haku, haku)
        counter = 0
        cursor.execute(query)
        for data in cursor:
            counter += 1
            lista += keys1[data[0]] + " - " + data[1] + " - " + data[3] + "\n"
        if counter == 1:
            url = "http://telok.dsvr.org/datasheets/" + data[1] + ".pdf"
            update.message.reply_document(url)

        else:
            lista += "Total results: " + str(counter)
        update.message.reply_text(lista)
        cursor.close()
        cnx.close()
    except IndexError:
        lista = "Usage: /telok <search>\n"
        lista += "Current component types in the database:\n"
        for avain in sorted(keys2.keys()):
            lista += avain + "\n"
        update.message.reply_text(lista)