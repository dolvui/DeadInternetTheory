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
        await b.save_cookies()
        b.browser.stop()

async def create_video(account = 0):
    b = bw.Browser(globals.SESSIONS_PATH["chrome_path"],globals.SESSIONS_PATH["pix_account"][account])
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

    textbox_voix = await b.current_page.find_elements_by_text('Bonjour à tous')
    textbox_prompt = await b.current_page.find_elements_by_text('Décrivez le contenu que vous souhaitez créer')

    print(textbox_voix)
    print(textbox_prompt)
    
    await textbox_voix[1].mouse_click()  # Focus the field
    await textbox_voix[1].send_keys("test1\n")

    await textbox_prompt[1].mouse_click()  # Focus the field
    await textbox_prompt[1].send_keys("test2\n")

    await asyncio.sleep(10)