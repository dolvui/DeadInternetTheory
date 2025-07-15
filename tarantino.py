import asyncio

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

async def create_video(account):
    b = bw.Browser(globals.SESSIONS_PATH["chrome_path"],account)
    await b.init_browser()
    await b.load_cookies()
    await b.load_page(globals.SESSIONS_PATH["links"]["HOME_STUDIO"], 5)

    await b.load_page(globals.SESSIONS_PATH["links"]["STUDIO"],5)
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

    not_posted = globals.db.get_not_posted_videos()

    textbox_voix = await b.current_page.find_elements_by_text('Bonjour à tous')
    textbox_prompt = await b.current_page.find_elements_by_text('Décrivez le contenu que vous souhaitez créer')
    
    await textbox_voix[1].mouse_click()  # Focus the field
    await textbox_voix[1].send_keys(not_posted[2])

    await textbox_prompt[1].mouse_click()  # Focus the field
    await textbox_prompt[1].send_keys(not_posted[1])

    await asyncio.sleep(1)

    #TODO press creer !

    while(await b.current_page.find_elements_by_text('en cours de generation')):
        await asyncio.sleep(1)

    #TODO telecharger et mettre a jour la database