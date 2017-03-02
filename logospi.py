from picamera import PiCamera
from time import sleep
import logosshorties


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