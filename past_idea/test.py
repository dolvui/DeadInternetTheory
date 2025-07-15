import asyncio
import keyword

import nodriver as uc
from bs4 import BeautifulSoup
import os
import requests
import yt_dlp
import random
import sys

COOKIE_FILE_NAME = "../sessions/.session.dat"

async def load_cookies(browser, page):
    try:
        await browser.cookies.load(COOKIE_FILE_NAME)
        await page.reload()
        print("Cookies loaded.")
        return True
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Failed to load cookies: {e}")
    except FileNotFoundError:
        print("Cookie file does not exist.")

    return False


async def save_cookies(browser):
    try:
        await browser.cookies.save(COOKIE_FILE_NAME)
        print("Cookies saved.")
    except Exception as e:
        print(f"Failed to save cookies: {e}")


def download_video(url,var ,save_path="C:"):
    headers = {
        "User-Agent": "okhttp"
    }

    filepath = os.path.join(save_path + "\\downloaded"+ f"_{var}" +".mp4")

    ydl_opts = {
        'outtmpl': filepath,
        'format': 'bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/best',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'noplaylist': True,
        'quiet': False,
        'extractor_args': {'tiktok': {'webpage_download': True}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"\nVideo successfully downloaded: {save_path}")
            return save_path

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return None

async def publish_video():

    print(f"Starting for publishing video")
    browser = await uc.start(browser_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    print("Browser started successfully")

    page = await browser.get("https://www.tiktok.com/tiktokstudio/upload?from=webapp")

    await load_cookies(browser,page);
    print("TikTok profile page loaded successfully")

    await asyncio.sleep(4)

    print("Waited for 10 seconds to allow content to load")

    button = await page.find_elements_by_text('input[type="file"]');

    await asyncio.sleep(2)

    await button[0].send_file('C:')
    #await button.click()

    await asyncio.sleep(2)

    script = '''
    var elem = document.querySelector('span[data-text="true"]');
    if (elem) {
        elem.innerText = "quelle dingerie";
    }
    '''
    await page.evaluate(script);

    await asyncio.sleep(2)

    sendButton = await page.find_elements_by_text('Publier')
    await asyncio.sleep(1)

    print(sendButton)
    await sendButton[1].click();

    await asyncio.sleep(10)
    print('end for now')


async def scrape_tiktok_profile(username):
    try:
        print(f"Initiating scrape for TikTok profile: @{username}")
        browser = await uc.start(headless=False,
                                 browser_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                                 no_sandbox=True)
        print("Browser started successfully")

        page = await browser.get(f"https://www.tiktok.com/@{username}")
        print("TikTok profile page loaded successfully")

        await asyncio.sleep(10)  # Wait for 10 seconds
        print("Waited for 10 seconds to allow content to load")

        html_content = await page.evaluate('document.documentElement.outerHTML')
        print(f"HTML content retrieved (length: {len(html_content)} characters)")

        soup = BeautifulSoup(html_content, 'html.parser')
        print("HTML content parsed with BeautifulSoup")

        video_links = []
        for link in soup.find_all('a', href=True):
            if(link['href'].startswith('https://www.tiktok.com')):
                video_links.append(link['href'])

        c = 0;
        for link in video_links:
            print(f"downloading video link: {link}")
            download_video(link,c);
            c= c+1;
        return video_links
    except Exception as e:
        print(f"An error occurred while scraping: {str(e)}")
        return None

    finally:
        if 'browser' in locals():
            browser.stop()
        print("Browser closed")

async def idle_brain_rot():
    print("Starting brain rotting")
    browser = await uc.start(browser_executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")

    await asyncio.sleep(5)

    page = await browser.get("https://www.tiktok.com/foryou")

    await load_cookies(browser, page);
    print("Cookie loaded successfully")

    #await asyncio.sleep(10)

    buttonLike = await page.find_elements_by_text("Laisser un j'aime sur la vidéo");
    buttonFollow = await page.select_all('button[shape="capsule"]');

    while(True):
        print("----------brain rooooooooooooooooooooooot me ------------------------------------")

        buttonNext = await page.select_all('button[class="TUXButton TUXButton--capsule TUXButton--medium TUXButton--secondary action-item css-1egy55o"]');

        await asyncio.sleep(random.randint(1,2))

        if(random.randint(1,3) == 3):
            print("like")
            #await buttonLike[0].click();
            await buttonLike[0].click_mouse();

        await asyncio.sleep(random.randint(1, 3))

        if(random.randint(1,5) == 2):
            print("follow")
            await buttonFollow[0].click_mouse();
            #await buttonFollow[0].click();

        await asyncio.sleep(random.randint(1, 4))
        print("next")

        if(len(buttonNext) >= 2):
            await buttonNext[1].click();
        else:
            await buttonNext[0].click();


async def main():
    #await publish_video()
    await idle_brain_rot();
    username = "temsa.31"
    #profile_info = await scrape_tiktok_profile(username)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
