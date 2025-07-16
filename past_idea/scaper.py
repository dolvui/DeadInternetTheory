import os
from datetime import datetime

import yt_dlp
from bs4 import BeautifulSoup


def download_video(url,var ,db,save_path="C:"):
    headers = {
        "User-Agent": "okhttp"
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"downloaded_{timestamp}_{var}.mp4"

    filepath = os.path.join(save_path +filename)

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
            db.add_video(url,filepath);
            return save_path

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return None

async def scrape_tiktok_profile(usernames,b,db):
    for username in usernames:
        try:
            await b.load_page(f"https://www.tiktok.com/@{username}",10)

            html_content = await b.current_page.evaluate('document.documentElement.outerHTML')

            soup = BeautifulSoup(html_content, 'html.parser')

            video_links = []
            for link in soup.find_all('a', href=True):
                if(link['href'].startswith('https://www.tiktok.com')):
                    video_links.append(link['href'])
            c = 0;
            for link in video_links:
                print(f"downloading video link: {link}")
                download_video(link,c,db);
                c= c+1;
            return video_links
        except Exception as e:
            print(f"An error occurred while scraping: {str(e)}")
            return None

async def scrape_youtube_profile(db,b):
    users = db.get_not_scraped_users()
    await scrape_tiktok_profile(users,b,db)
    db.users_done(users)
