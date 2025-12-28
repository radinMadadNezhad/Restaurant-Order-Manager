from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # 1. Capture Home Page
        print("Navigating to Home Page...")
        page.goto("http://127.0.0.1:8000/")
        page.screenshot(path="docs/screenshots/home_page.png")
        print("Captured docs/screenshots/home_page.png")

        # 2. Login to get to Dashboard
        print("Logging in...")
        page.goto("http://127.0.0.1:8000/accounts/login/")
        page.fill("input[name='username']", "admin_test")
        page.fill("input[name='password']", "password123")
        page.click("button[type='submit']")
        
        # Wait for navigation to dashboard
        page.wait_for_url("**/dashboard/")
        
        # 3. Capture Dashboard
        # Make the viewport a bit larger to capture the full dashboard nicely
        page.set_viewport_size({"width": 1280, "height": 800})
        # Wait a moment for any potential animations or loads
        time.sleep(1) 
        
        # Taking screenshot
        print("Capturing Dashboard...")
        page.screenshot(path="docs/screenshots/dashboard.png")
        print("Captured docs/screenshots/dashboard.png")

        browser.close()

if __name__ == "__main__":
    run()
