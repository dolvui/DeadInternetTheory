import brower_wrapper as bw
import asyncio
import keyword
from bs4 import BeautifulSoup
import os
import requests
import yt_dlp
import random
import sys
import json
import database
from datetime import datetime

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

COOKIE_PIXIE_ONE = ".session_pixie_one.dat"
COOKIE_PIXIE_TWO = ".session_pixie_two.dat"

video_data = "singe_videos_ia.json"
studio = "https://app.pixverse.ai/create/image-text"
home_studio = "https://app.pixverse.ai/home"

async def retrieve_credit():
    b = bw.Browser(chrome_path,COOKIE_PIXIE_ONE)
    await b.init_browser()
    await b.load_cookies()
    await b.load_page(home_studio,5)
    await b.save_cookies()
    b.browser.stop()

    b2 = bw.Browser(chrome_path, COOKIE_PIXIE_TWO)
    await b2.init_browser()
    await b2.load_cookies()
    await b2.load_page(home_studio, 5)
    await b2.save_cookies()
    b2.browser.stop()

async def create_video():
    return