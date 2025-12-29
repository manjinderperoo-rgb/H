import asyncio
import argparse
import sys
from playwright.async_api import async_playwright, TimeoutError

USER_DATA_DIR = "browser_data"

EDIT_BUTTON_NAME = "Click to edit group subject"
RETRY_DELAY = 1.5
MAX_RETRY = 999999  # practically infinite

async def click_edit_button(page):
    for attempt in range(MAX_RETRY):
        try:
            btn = page.get_by_role("button", name=EDIT_BUTTON_NAME)
            await btn.wait_for(timeout=5000)
            await btn.click()
            return True
        except TimeoutError:
            print("⚠️ Edit button not found, retrying...")
        except Exception as e:
            print(f"⚠️ Click error: {e}")
        await asyncio.sleep(RETRY_DELAY)

async def clear_and_fill(page, text):
    for attempt in range(MAX_RETRY):
        try:
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Backspace")
            await page.keyboard.type(text, delay=50)
            await page.keyboard.press("Enter")
            return True
        except Exception as e:
            print(f"⚠️ Keyboard error: {e}")
            await asyncio.sleep(RETRY_DELAY)

async def main(names):
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        page = context.pages[0] if context.pages else await context.new_page()

        print("Browser ready ✅")
        print("Type 'Ready' to start automation")

        while True:
            if input("> ").strip().lower() == "ready":
                break

        print("Automation started 🔁  (Ctrl + C to stop)")

        index = 0

        try:
            while True:
                name = names[index % len(names)]
                index += 1

                await click_edit_button(page)
                await asyncio.sleep(0.5)
                await clear_and_fill(page, name)

                print(f"✅ Name updated → {name}")
                await asyncio.sleep(2)

        except KeyboardInterrupt:
            print("\n🛑 Ctrl + C detected, closing...")
            await context.close()
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--names",
        required=True,
        help="Comma separated names"
    )

    args = parser.parse_args()
    names_list = [n.strip() for n in args.names.split(",") if n.strip()]

    if not names_list:
        print("❌ No valid names provided")
        sys.exit(1)

    asyncio.run(main(names_list))
