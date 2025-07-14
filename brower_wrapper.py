import nodriver as uc
import asyncio

class Browser:
    def __init__(self, browser_url: str, cookie_file: str):
        self.browser_url = browser_url
        self.cookie_file = cookie_file
        self.browser = None
        self.current_page = None
        self.cookies_loaded = False

    async def init_browser(self):
        self.browser = await uc.start(
            headless=False,
            browser_executable_path=self.browser_url,
            no_sandbox=True
        )
        print("Browser initialized.")

    async def save_cookies(self,wait = 5):
        await asyncio.sleep(wait)
        try:
            await self.browser.cookies.save(self.cookie_file)
            print("Cookies saved.")
        except Exception as e:
            print(f"Failed to save cookies: {e}")

    async def load_cookies(self):
        try:
            print("Loading cookies...")
            await self.browser.cookies.load(self.cookie_file)
            if self.current_page:
                await self.current_page.reload()
            self.cookies_loaded = True
            print("Cookies loaded successfully.")
        except Exception as e:
            print(f"Cookie load failed: {e}")

    async def load_page(self, url: str, wait: float = 1.0):
        print(f"Navigating to {url}...")
        self.current_page = await self.browser.get(url)
        await asyncio.sleep(wait)
        if not self.cookies_loaded:
            await self.load_cookies()
        return self.current_page
