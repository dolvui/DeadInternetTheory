import asyncio
from nodriver import cdp

import globals


async def publish_random_video(b):
    video = globals.db.get_generate_video()

    if not video:
        print("No new videos")
    else:
        await publish_video(b, video[0], video[5], video[4])

async def publish_video(b,video_id,video_path,video_description):

    await b.load_page(globals.SESSIONS_PATH["social_post_path"], 15)

    button = await b.current_page.find_elements_by_text('input[type="file"]')

    await asyncio.sleep(2)

    await button[0].send_file(video_path)

    await asyncio.sleep(2)

    #set description

    textbox = await b.current_page.find_elements_by_text('downloaded')

    await textbox[1].mouse_click()  # Focus the field

    await clear_text(b)

    await textbox[1].send_keys(video_description)

    await asyncio.sleep(2)

    await b.current_page.send(cdp.runtime.evaluate(
        expression="window.scrollTo(0, document.body.scrollHeight)"
    ))

    sendButtons = await b.current_page.select_all('button[role="button"]')

    for sendButton in sendButtons:
        if sendButton.text == "Publication" or sendButton.text == "Post":
            await asyncio.sleep(3)

            await sendButton.scroll_into_view()

            await sendButton.click()

            await sendButton.mouse_click()

    globals.db.mark_video_as_posted(video_id)
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
