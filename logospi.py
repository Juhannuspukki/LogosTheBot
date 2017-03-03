from picamera import PiCamera
from time import sleep
import logosshorties
import RPi.GPIO as GPIO
import json
from datetime import datetime


def cam(bot, update):
    chat_id = str(update.message.chat_id)
    camera = PiCamera()
    camera.resolution = (1920, 1080)
    camera.vflip = True
    camera.hflip = True
    camera.start_preview()
    bot.sendChatAction(chat_id, 'upload_photo')
    sleep(3)
    camera.capture('/home/pi/Desktop/Logos/justnow.jpg')
    camera.stop_preview()
    photo = "/home/pi/Desktop/Logos/justnow.jpg"
    logosshorties.sendphotohelper(bot, update, chat_id, photo)
    camera.close()


def alaoviauki(bot, update):
    chat_id = str(update.message.chat_id)

    with open('logosmastercontrol.json', 'r') as fp:
        mastercontrol = json.load(fp)

    if chat_id in mastercontrol["accesscontrol"]:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3, GPIO.OUT)
        GPIO.output(3, GPIO.HIGH)
        update.message.reply_text("Executing...")
        sleep(1)
        GPIO.output(3, GPIO.LOW)
        update.message.reply_text("Success.")
        GPIO.cleanup()
    else:
        update.message.reply_text("Unauthorized. This incident will be reported.")
        now = str(datetime.now())
        käyttäjä = update.message.from_user
        data = now + ", " + str(käyttäjä.id) + ", " + käyttäjä.first_name + ", " + käyttäjä.last_name + \
            ", " + käyttäjä.username + "\n"

        with open('unauthorizedaccesslist.txt', 'a') as file:
            file.write(data)
