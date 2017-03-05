import datetime
import json
import requests
import re
from lxml import html


def newton(bot, update):
    update.message.reply_text(juvenes())


def juvenes(KitchenId="6", MenuTypeId="60"):
    try:
        date = str(datetime.date.today())
        day = date[8:]
        month = date[5:7]

        teksti = ""
        url = "http://www.juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByDate?KitchenId=" \
              + KitchenId + "&MenuTypeId=" + MenuTypeId + "&Date='" + day + "/" + month + "'&lang='fi'&format=json"
        x = requests.get(url)
        x = x.content.decode("utf-8")

        menu = json.loads(x, encoding='utf-8')

        a = menu["MealOptions"]
        for i in range(len(a)):
            b = a[i]
            c = b["MenuItems"]
            d = c[0]
            e = d["Name"]
            e2 = d["Diets"]
            teksti += "• " + e + " " + e2 + "\n"

        if not teksti:
            teksti = "Ei mitään syötävää!\n\n"
    except ValueError:
        teksti = "Ei mitään syötävää!\n\n"
    return teksti


def menu(bot, update):
    päämuuttuja = "Newtonissa tarjolla:\n\n"

    date = str(datetime.date.today())
    day = date[8:]
    month = date[5:7]
    year = date[:4]

    päämuuttuja += juvenes("6", "60")
    päämuuttuja += "Ravintola Newton palvelee yleensä ma-to 10.30-16.00 ja pe 10.30-15.00" + "\n\n" + "Sååsibaarissa:\n\n"
    päämuuttuja += juvenes("60038", "77")
    päämuuttuja += "SÅÅSBAR on avoinna ma-pe 10.30-19.00" + "\n\n" + "Fusarissa:\n\n"
    päämuuttuja += juvenes("60038", "3")
    päämuuttuja += "Fusion Kitchen on avoinna ma-pe 10.30-18.45, Café Konehuone palvelee ma-pe klo 8-19" + "\n"

    päämuuttuja += "\n" + "Reaktori tarjoaa:" + "\n\n"
    url = "http://www.amica.fi/modules/json/json/Index?costNumber=0812&language=fi"
    x = requests.get(url)
    x = x.content.decode("utf-8")

    x = x.replace("  ", "")

    menu = json.loads(x, encoding='utf-8')
    a = menu["MenusForDays"]
    for i in range(len(a)):
        if date in a[i]["Date"]:
            b = a[i]
            c = b["SetMenus"]
            for ö in range(len(c)):
                d = c[ö]
                if d["Name"] not in päämuuttuja:
                    päämuuttuja += d["Name"] + ": " + "\n"
                e = d["Components"]
                for w in range(len(e)):
                    ruokalaji = e[w]
                    päämuuttuja += "    • " + ruokalaji + "\n"
            päämuuttuja = päämuuttuja.replace("xc2xb4", "'")
            päämuuttuja += "Reaktori on avoinna " + a[i]["LunchTime"] + "\n"

    päämuuttuja += "\n" + "Hertsissä tänään:" + "\n\n"
    url = "http://www.sodexo.fi/ruokalistat/output/daily_json/12812/" + year + "/" + month + "/" + day + "/fi"
    x = requests.get(url)
    x = x.content.decode("utf-8")

    menu = json.loads(x, encoding='utf-8')
    menu = menu["courses"]

    vanhouten = {}
    keylist = []
    for i in range(len(menu)):
        ööö = menu[i]
        try:
            temp_variable = "    • " + ööö["title_fi"] + " " + ööö["properties"] + "\n"
            vanhouten[temp_variable] = ööö["category"] + ": "
        except KeyError:
            temp_variable = "    • " + ööö["title_fi"] + "\n"
            vanhouten[temp_variable] = ööö["category"] + ": "

    for key in sorted(vanhouten.keys()):
        if vanhouten[key] not in keylist:
            päämuuttuja += vanhouten[key] + "\n" + key
            keylist.append(vanhouten[key])
        else:
            päämuuttuja += key

    päämuuttuja = päämuuttuja.replace("  ", " ")
    päämuuttuja += "Hertsi on avoinna Ma-Pe 10.30 - 15.00, kahvila Bitti palvelee klo 08.00 - 17.00 Ma-Pe"
    update.message.reply_text(päämuuttuja)


def liiga(bot, update):
    l = []

    page = requests.get("http://liiga.fi/tilastot/2016-2017/runkosarja/joukkueet/")
    tree = html.fromstring(page.content)
    check = tree.xpath('//td[@class="ta-l"]/text()')
    p = tree.xpath('//strong/text()')

    check = re.sub("\n", "", ("".join(check)))
    check = re.sub("      ", "", check)
    check = check.split("  ")
    del check[0]
    del check[0]

    for i in range(15):
        l.append(": ".join([check[i], p[i]]))

    l = ", ".join(l)
    update.message.reply_text(l)