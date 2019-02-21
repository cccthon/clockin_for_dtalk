from airtest.core.api import *
# import requests
import time
import schedule
import yaml
import os
from addict import Dict
# from wxpy import *
import logging
if not os.path.exists("logs"):
    os.makedirs("logs")
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
curr_month = time.strftime("%Y-%m", time.localtime(time.time()))
handler = logging.FileHandler("logs/clock_" + curr_month + ".log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)

conf = Dict(yaml.load(open("clockin.yml","r",encoding='utf-8')))

"""
adb shell ps| grep "com.alibaba.android.rimet"
adb shell am force-stop "com.alibaba.android.rimet"
"""


def sendMsg_wx(msg=''):
    wechat = Bot(console_qr=2,cache_path="botoo.pkl")
    # print(help(wechat))
    wechat.file_helper.send(msg)

def connect_byWiff(mobileAddr=conf.mobileAddr,port=conf.port):
    con = connect_device("Android:///" + mobileAddr + ":" + port)
    return con

def unlock_byNum(dev,passwd=conf.passwd):
    logger.info("device connected.")
    dev.shell("input keyevent KEYCODE_POWER")   #
    dev.wake()
    time.sleep(0.3)
    dev.shell("input swipe 550 1500 550 200")
    time.sleep(0.3)
    for i in str(passwd):
        dev.shell("input text KEYCODE_" + str(i))

def auto_clockin(dev):
    # devices = device()
    # print("adb devices: ", devices.list_app())
    # install(apkName)
    dev.home()
    dev.stop_app(conf.apkName)
    time.sleep(0.3)
    dev.start_app(conf.apkName)
    time.sleep(6)
    dev.home()
    dev.shell("input keyevent KEYCODE_POWER")
    logger.info("clockin success.")

def on_off_duty():
    curr_hour = time.strftime("%H:%M", time.localtime(time.time()))
    if curr_hour > "00:00" and curr_hour < conf.onDuty:
        return 0
    elif curr_hour > conf.onDuty and curr_hour < "23:59":
        return 1

def job_clockin():
    # """
    logger.info("start connect device: " + conf.mobileAddr+ ":" + conf.port)
    while True:
        try:
            # dev = connect_device("Android:///" + mobileAddr + ":" + port)
            dev = connect_byWiff()
        except:
            curr_hour = time.strftime("%H:%M", time.localtime(time.time()))
            if on_off_duty() == 0:
                if curr_hour > conf.onDuty:
                    break
            if on_off_duty() == 1:
                if curr_hour > conf.offDuty_poling_endTime:
                    break
            logger.info("devices connect fail.retrying...")
            time.sleep(conf.interval)
            # time.sleep(3)
            continue
        else:
            unlock_byNum(dev)
            auto_clockin(dev)
            break


if __name__ == '__main__':

    schedule.every().day.at(conf.onDuty_polling_startTime).do(job_clockin)
    schedule.every().day.at(conf.offDuty).do(job_clockin)
    # print(on_off_duty())
    while True:
        curr_hour = time.strftime("%H:%M", time.localtime(time.time()))
        if curr_hour < conf.onDuty_polling_startTime or curr_hour > conf.offDuty:
            logger.info("pending... next clockin time at: " + conf.onDuty_polling_startTime)
        elif curr_hour > conf.onDuty_polling_startTime and curr_hour < conf.offDuty:
            logger.info("pending... next clockin time at: " + conf.offDuty)
        schedule.run_pending()
        time.sleep(60)   
    
    # job_clockin()