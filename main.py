import random
import traceback

import brower_wrapper as bw
import nodriver as uc
from enum import Enum

import scaper
import gather
import asyncio
import database
import uploader
import tarantino
import monkeydb

COOKIE_FILE_NAME = ".session.dat"
COOKIE_PIXIE_ONE = ".session_pixie_one.dat"
COOKIE_PIXIE_TWO = ".session_pixie_two.dat"

db = monkeydb.monkeyDB()

async def main_load_json(path):
    try:
        db.fill_database_form_json(path)
        print("json file loaded successfully !")
    except:
        traceback.print_exc()

async def main_credit():
    try:
        await tarantino.retrieve_credit()
        print("credits retrieve successfully !")
    except:
        traceback.print_exc()

async def main_create():
    try:
        await tarantino.create_video()
        print("video create successfully !")
    except:
        traceback.print_exc()

async def main_post():
    b = bw.Browser("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",COOKIE_FILE_NAME)
    await b.init_browser()
    await b.load_cookies()
    await uploader.publish_random_video(b,db)

async def main_register(session):
    b = bw.Browser("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", session)
    await b.init_browser()
    await b.load_cookies()
    await asyncio.sleep(120) # 2 min
    await b.save_cookies()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='select which action need to make')

    parser.add_argument('--load-json', metavar='path', required=False,help='the path of a json file to load into db')
    parser.add_argument('--pix-credit', required=False, help='to retrieve credit form the IA site')
    parser.add_argument('--post', required=False, help='TO post a video on tiktok')
    parser.add_argument('--create', required=False, help='create a new video')
    parser.add_argument('--register', required=False, help='You got 2 min to register on a account')

    args = parser.parse_args()

    if(args.post):
        print("Let's post a video !")
        uc.loop().run_until_complete(main_post())
    if (args.pix_credit):
        print("let's retrieve some credit !")
        uc.loop().run_until_complete(main_credit())
    if (args.load_json):
        print("let's load a json file !")
        uc.loop().run_until_complete(main_load_json(args.load_json))
    if (args.create):
        print("let's create a new video !")
        uc.loop().run_until_complete(main_create())
    if (args.register):
        print("let's register on a website!")
        uc.loop().run_until_complete(main_register(args.register))