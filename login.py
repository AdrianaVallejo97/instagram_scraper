from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.instagram.com/accounts/login/")

    print("Inicia sesión manualmente")
    input("Presiona ENTER cuando termines")

    context.storage_state(path="state.json")

    browser.close()