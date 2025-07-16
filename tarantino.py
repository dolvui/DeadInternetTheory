import asyncio
from datetime import datetime
import yt_dlp
import os

import brower_wrapper as bw
import globals


async def retrieve_credit():
    data = globals.SESSIONS_PATH
    for session in data["pix_account"]:

        b = bw.Browser(globals.SESSIONS_PATH["chrome_path"],session)
        await b.init_browser()
        await b.load_cookies()
        await asyncio.sleep(2)
        await b.load_page(globals.SESSIONS_PATH["links"]["HOME_STUDIO"],5)
        credit = await b.current_page.select('span[class="text-text-credit"]')
        globals.db.update_or_create_account(session,int(credit.text))
        await b.save_cookies()
        b.browser.stop()

async def create_video(account,video_path):
    b = bw.Browser(globals.SESSIONS_PATH["chrome_path"],account)
    await b.init_browser()
    await b.load_cookies()
    await b.load_page(globals.SESSIONS_PATH["links"]["HOME_STUDIO"], 5)

    await b.load_page(globals.SESSIONS_PATH["links"]["STUDIO"],5)
    await b.current_page.fullscreen()

    await asyncio.sleep(3)

    duration = await b.current_page.find('8s',best_match=True)
    format = await b.current_page.find('9:16',best_match=True)
    res = await b.current_page.find('360P',best_match=True)

    switch = await b.current_page.select_all('button[role="switch"]')

    await duration.mouse_click()
    await format.mouse_click()
    await res.mouse_click()

    await switch[0].mouse_click() # sound design
    #await switch[1].mouse_click()

    await asyncio.sleep(3)

    not_posted = globals.db.get_not_generate_video()

    #textbox_voix = await b.current_page.find_elements_by_text('Bonjour à tous')
    textbox_prompt = await b.current_page.find_elements_by_text('Décrivez le contenu que vous souhaitez créer')
    textbox_sound = await b.current_page.find_elements_by_text('[Optionnel]Décrivez l\'effet sonore, par exemple')

    await textbox_sound[1].mouse_click()
    await textbox_sound[1].send_keys(not_posted[6])

    #await textbox_voix[1].mouse_click()
    #await textbox_voix[1].send_keys(not_posted[2])

    await textbox_prompt[1].mouse_click()
    await textbox_prompt[1].send_keys(not_posted[1])

    await asyncio.sleep(1)

    create_button = await b.current_page.find('Créer', best_match=True)

    # comment to not burn all credit during test
    await create_button.mouse_click()

    print("wait 10 sec")
    await asyncio.sleep(10)

    new_video = await b.current_page.find('Votre vidéo est en cours de génération',best_match=True)
    position = None
    while new_video:
        try:
            new_video = await b.current_page.find('Votre vidéo est en cours de génération',best_match=True)
            position = await new_video.get_position()
        except Exception as e:
            print(e)
        await asyncio.sleep(1)

    await b.current_page.mouse_click(position.x,position.y)
    await asyncio.sleep(3)

    links = await b.current_page.find_elements_by_text('.mp4')
    await download_video(links[0].src,video_path,not_posted[0])

    #globals.db.update_account_credit(account,60)

async def download_video(url,save_path,video_id):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"downloaded_{timestamp}.mp4"

    filepath = os.path.join(save_path + '\\' + filename)

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
            globals.db.set_video_path(filepath,video_id)
            return save_path

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return None