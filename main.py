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

COOKIE_FILE_NAME = ".session.dat"

COOKIE_PIXIE_ONE = ".session_pixie_one.dat"
COOKIE_PIXIE_TWO = ".session_pixie_two.dat"

async def main():
    # b = bw.Browser("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",COOKIE_FILE_NAME)
    # await b.init_browser()
    # await b.load_cookies()
    await tarantino.retrieve_credit()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
















#db = database.VideoDB()

# class State(Enum):
#     START = 0
#     ROT = 1
#     SCRAP = 2
#     UPLOAD = 3
#     WAIT = 4
#
# async def robot(b):
#     state = State.UPLOAD
#     run = 1
#     while run:
#         try:
#             match state:
#                 case State.START:
#                     state = State.ROT
#                     # if random.randint(1,100) == 69:
#                     #     run = 0
#                 case State.ROT:
#                     await gather.rooting(b, random.randint(30,90))
#                     state = State.SCRAP
#                 case State.SCRAP:
#                     #await scaper.scrape_youtube_profile(db, b)
#                     state = State.UPLOAD
#
#                 case State.UPLOAD:
#                     await uploader.publish_random_video(b, db)
#                     state = State.WAIT
#
#                 case State.WAIT:
#                     print("pause")
#                     await asyncio.sleep(random.randint(10,60 *5 ))
#                     state = State.START
#                 case _ :
#                     continue
#         except Exception:
#             await b.current_page.reload();
#             print("Error while : " ,state , '\n' ,traceback.format_exc())
