import brower_wrapper as bw
from nodriver import Element
import asyncio
import random
import json
import database

db = database.VideoDB()

async def rooting(b,round):
    await b.load_page("https://www.tiktok.com/foryou",5)

    for _ in range(round):
        print("-- New round --")
        buttonLike = await b.current_page.find_elements_by_text("Laisser un j'aime sur la vidéo");
        buttonFollow = await b.current_page.select_all('button[shape="capsule"]');
        buttonNext = await find_next_button(b.current_page)


        seed = random.randint(1, 70)
        delay = int(random.randint(1,seed)/10);

        if seed <= 30 and buttonLike:
            print("like")
            await buttonLike[0].click()

        await asyncio.sleep(seed/10)

        if seed <= 10 and buttonFollow:
            print("follow")
            await buttonFollow[-1].click()


        username = await b.current_page.select_all('div[data-e2e="video-author-uniqueid"]')
        if username:
            print(f"save {username[0].text}")
            db.add_user(username[0].text)
        else:
            print("Username not found.")

        await buttonNext.click()
        await asyncio.sleep(seed/10 + delay)
        await b.save_cookies()

    return True;

async def find_next_button(page):
    buttons :List[Element] = await page.select_all("button[type='button'][aria-disabled='false']")
    for btn in buttons:
        if btn:
            html = await btn.get_html()
            if 'path d="m24 27.76' in html:  # SVG down arrow path
                return btn
    return None




### NOT USED DONT WORK :


async def get_visible_article(page):
    articles = await page.select_all('article')
    print(len(articles))
    for article in articles:
        # Run JS inside browser context to check visibility
        top = await article.apply("e => e.getBoundingClientRect().top")
        if 0 <= top <= 20:  # near top of viewport
            return article
    return None

async def extract_username_from_article(article):
    a_tags = await article.select_all('a[href^="/@"]')
    for a_tag in a_tags:
        try:
            username = await a_tag.get_text();
            print(username)
            href = await a_tags.get_attribute("href")
            print(href)
        except:
            continue

    # if a_tags:
    #     href = await a_tags[0].get_attribute("href")
    #     if href:
    #         return href.lstrip("/@").split("/")[0]
    # return None

async def extract_video_metadata(page):
    article = await get_visible_article(page)
    if not article:
        return None

    # Username
    username = await extract_username_from_article(article)

    # Caption
    caption_elem = await article.select_all('div[data-e2e="browse-video-desc"]')
    caption = await caption_elem[0].text() if caption_elem else ""

    # Video src
    video_elem = await article.select_all("video")
    video_src = await video_elem[0].get_attribute("src") if video_elem else ""

    return {
        "username": username,
        "caption": caption,
        "video_url": video_src
    }
