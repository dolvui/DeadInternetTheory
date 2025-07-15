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

    await asyncio.sleep(3)

    duration = await b.current_page.find('8s',best_match=True)
    format = await b.current_page.find('9:16',best_match=True)
    res = await b.current_page.find('360P',best_match=True)

    switch = await b.current_page.select_all('button[role="switch"]')

    await duration.mouse_click()
    await format.mouse_click()
    await res.mouse_click()

    await switch[0].mouse_click()
    await switch[1].mouse_click()

    await asyncio.sleep(3)

    not_posted = globals.db.get_not_generate_video()

    textbox_voix = await b.current_page.find_elements_by_text('Bonjour à tous')
    textbox_prompt = await b.current_page.find_elements_by_text('Décrivez le contenu que vous souhaitez créer')
    
    await textbox_voix[1].mouse_click()
    await textbox_voix[1].send_keys(not_posted[2])

    await textbox_prompt[1].mouse_click()
    await textbox_prompt[1].send_keys(not_posted[1])

    await asyncio.sleep(1)

    create_button = await b.current_page.find('Créer', best_match=True)

    # comment to not burn all credit during test
    #create_button.mouse_click()

    while(await b.current_page.find_elements_by_text('en cours de generation')):
        await asyncio.sleep(1)

    #TODO telecharger et mettre a jour la database