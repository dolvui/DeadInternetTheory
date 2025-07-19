import asyncio
import nodriver as uc
import random
import logging

import brower_wrapper as bw
import tarantino
import uploader
import globals

sessions_directory = "sessions\\"

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)

async def main_load_json(path):
    try:
        globals.db.fill_database_form_json(path)
        print("json file loaded successfully !")
        return 0
    except Exception as e:
        print(e)
        return -1

async def main_load_json_veo(path):
    try:
        globals.db.fill_database_form_json(path)
        print("json file loaded successfully !")
        return 0
    except Exception as e:
        print(e)
        return -1

async def main_credit():
    try:
        await tarantino.retrieve_credit()
        print("credits retrieve successfully !")
        return 0
    except Exception as e:
        print(e)
        return -1

async def main_create(video_path,credit = 60):
    try:
        accounts = globals.db.find_sufficient_account(credit)

        if not accounts or len(accounts) == 0:
            print("no accounts have sufficient credit !")
            return 1
        else:
            account = random.choice(accounts)
            await tarantino.create_video(account,video_path)
            print("video create successfully !")
            return 0
    except Exception as e:
        print(e)
        return -1

async def main_post(account):
    try:
        b = bw.Browser(globals.SESSIONS_PATH["chrome_path"],globals.SESSIONS_PATH[account])
        await b.init_browser()
        await b.load_cookies()
        await uploader.publish_random_video(b)
        return 0
    except Exception as e:
        print(e)
        return -1

async def main_register(new_session):
    try:
        new_path = sessions_directory + new_session
        b = bw.Browser(globals.SESSIONS_PATH["chrome_path"], new_path)
        await b.init_browser()
        await asyncio.sleep(120) # 2 min
        await b.save_cookies()
        return 0
    except Exception as e:
        print(e)
        return -1

if __name__ == "__main__":
    import argparse
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info("Starting program at: " + timestamp)

    parser = argparse.ArgumentParser(description='select which action need to make')

    parser.add_argument('--load-json', metavar='path', required=False,help='the path of a json file to load into db')
    parser.add_argument('--load-json-veo', metavar='path', required=False, help='the path of a json file to load into db for veo')
    parser.add_argument('--pix-credit', required=False, help='to retrieve credit form the IA site')
    parser.add_argument('--post', required=False, help='To post a video on tiktok')
    parser.add_argument('--create', required=False, help='create a new video')
    parser.add_argument('--create-veo', required=False, help='create a new video for veo')
    parser.add_argument('--credit', required=False, help='select credit plan')
    parser.add_argument('--register', required=False, help='You got 2 min to register on a account')
    parser.add_argument('--sessions-path', required=True, help='path to a json that contains .dat files names')

    args = parser.parse_args()

    globals.init(args.sessions_path)

    if args.post:
        print("Let's post a video !")
        logger.info(f"call with post {args.post}")
        uc.loop().run_until_complete(main_post(args.post))
    if args.pix_credit:
        print("let's retrieve some credit !")
        logger.info(f"call with pix_credit {args.pix_credit}")
        uc.loop().run_until_complete(main_credit())
    if args.load_json:
        logger.info(f"call with load_json {args.load_json}")
        print("let's load a json file !")
        uc.loop().run_until_complete(main_load_json(args.load_json))
    if args.load_json_veo:
        logger.info(f"call with load_json {args.load_json_veo}")
        print("let's load a json file !")
        uc.loop().run_until_complete(main_load_json_veo(args.load_json_veo))
    if args.create:
        logger.info(f"call with create {args.create}")
        print("let's create a new video !")
        if args.credit:
            uc.loop().run_until_complete(main_create(args.create,int(args.credit)))
        else:
            uc.loop().run_until_complete(main_create(args.create))
    if args.create_veo:
        logger.info(f"call with create {args.create}")
        print("let's create a new video !")
        #uc.loop().run_until_complete(main_create(args.create_veo))
    if args.register:
        logger.info(f"call with register {args.register}")
        print("let's register on a website!")
        uc.loop().run_until_complete(main_register(args.register))