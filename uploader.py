from selenium.webdriver.common.devtools.v85.dom import scroll_into_view_if_needed

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
from nodriver import cdp

def delete_file_if_exists(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted video: {path}")

async def publish_random_video(b,db):
    videos = db.get_videos_not_publish()
    video = random.choice(videos)
    await publish_video(video[1], b, db, video[0])


async def publish_videos(b,db):
    videos = db.get_videos_not_publish()
    for video in videos:
        await publish_video(video[1],b,db,video[0])

async def publish_video(path,b,db,video_id):
    print(f"Starting for publishing video")

    await b.load_page("https://www.tiktok.com/tiktokstudio/upload?from=webapp", 6)

    button = await b.current_page.find_elements_by_text('input[type="file"]');

    await asyncio.sleep(2)
    #print(button)
    await button[0].send_file(path)

    await asyncio.sleep(2)

    #set description

    textbox = await b.current_page.find_elements_by_text('downloaded')

    await textbox[1].mouse_click()  # Focus the field

    await clear_text(b);

    await textbox[1].send_keys("abonne toi #meme\n")

    await asyncio.sleep(2)

    await b.current_page.send(cdp.runtime.evaluate(
        expression="window.scrollTo(0, document.body.scrollHeight)"
    ))

    sendButtons = await b.current_page.select_all('button[role="button"]')

    for sendButton in sendButtons:
        if sendButton.text == "Publication":
            await asyncio.sleep(3)

            await sendButton.scroll_into_view()

            await sendButton.click();

            await sendButton.mouse_click()

    db.mark_video_posted(video_id)
    delete_file_if_exists(path)

    await asyncio.sleep(10)


async def clear_text(b):
    from nodriver import cdp

    # Ctrl+A
    await b.current_page.send(cdp.input_.dispatch_key_event(
        type_="keyDown",
        key="Control",
        code="ControlLeft",
        windows_virtual_key_code=17
    ))
    await b.current_page.send(cdp.input_.dispatch_key_event(
        type_="keyDown",
        key="a",
        code="KeyA",
        windows_virtual_key_code=65,
        modifiers=2
    ))
    await b.current_page.send(cdp.input_.dispatch_key_event(
        type_="keyUp",
        key="a",
        code="KeyA",
        windows_virtual_key_code=65,
        modifiers=2
    ))
    await b.current_page.send(cdp.input_.dispatch_key_event(
        type_="keyUp",
        key="Control",
        code="ControlLeft",
        windows_virtual_key_code=17
    ))

    # Delete
    await b.current_page.send(cdp.input_.dispatch_key_event(
        type_="keyDown",
        key="Delete",
        code="Delete",
        windows_virtual_key_code=46
    ))
    await b.current_page.send(cdp.input_.dispatch_key_event(
        type_="keyUp",
        key="Delete",
        code="Delete",
        windows_virtual_key_code=46
    ))
