from fontTools.varLib import set_default_weight_width_slant

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
    await b2.load_page(home_studio, 30)
    await b2.save_cookies()
    b2.browser.stop()

async def create_video(account = 1):
    b = bw.Browser(chrome_path,COOKIE_PIXIE_ONE if account == 1 else COOKIE_PIXIE_TWO )
    await b.init_browser()
    await b.load_cookies()
    await b.load_page(home_studio, 5)

    await b.load_page(studio,5)
    await b.current_page.fullscreen()

    await asyncio.sleep(5)

    duration = await b.current_page.find_elements_by_text('8s')
    format = await b.current_page.find_elements_by_text('9:16')
    res = await b.current_page.find_elements_by_text('360P')

    switch = await b.current_page.select_all('button[role="switch"]')

    await duration[1].mouse_click()
    await format[0].mouse_click()
    await res[0].mouse_click()

    await switch[0].mouse_click()
    await switch[1].mouse_click()

    textbox_voix = await b.current_page.find_elements_by_text('Bonjour à tous')
    textbox_prompt = await b.current_page.find_elements_by_text('Décrivez le contenu que vous souhaitez créer')

    print(textbox_voix)
    print(textbox_prompt)
    
    await textbox_voix[1].mouse_click()  # Focus the field
    await textbox_voix[1].send_keys("test1\n")

    await textbox_prompt[1].mouse_click()  # Focus the field
    await textbox_prompt[1].send_keys("test2\n")

    await asyncio.sleep(10)