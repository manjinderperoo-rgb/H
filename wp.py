import time
import keyboard
from playwright.sync_api import sync_playwright

USER_DATA_DIR = "browser_data"  # yahan cookies + session save hongi

def main():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://aws.amazon.com")

        print("Browser opened ✅")
        print("Ctrl + D dabao tabhi script close hogi")
        print("Tab tak kuch bhi nahi karega...")

        # === WAIT UNTIL CTRL + D ===
        keyboard.wait("ctrl+d")

        print("Ctrl + D detected ❌")
        context.close()

if __name__ == "__main__":
    main()
