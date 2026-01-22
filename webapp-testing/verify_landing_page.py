from playwright.sync_api import sync_playwright
import os

def run():
    print("Starting verification of Landing Page...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            url = 'http://localhost:8000'
            print(f"Navigating to {url}...")
            page.goto(url)
            page.wait_for_load_state('networkidle')
            
            # Screenshot
            screenshot_path = os.path.join(os.getcwd(), 'landing_page_verification.png')
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to: {screenshot_path}")
            
            # Verify Hero Title
            h1 = page.locator('h1.lp-hero-title')
            if h1.is_visible():
                print(f"SUCCESS: Hero title found.")
                print(f"Title Text: {h1.inner_text()}")
            else:
                print("FAILURE: Hero title h1.lp-hero-title not visible.")
                
            # Verify CTA Button
            btn = page.locator('a.lp-btn-primary', has_text="Begin Operations")
            if btn.is_visible():
                print("SUCCESS: 'Begin Operations' CTA button found.")
            else:
                print("FAILURE: 'Begin Operations' CTA button not found.")
                
            # Verify Feature Cards
            cards = page.locator('.lp-feature-card')
            count = cards.count()
            print(f"Found {count} feature cards.")
            if count >= 3:
                print("SUCCESS: Feature cards are present.")
            else:
                print("WARNING: Expected at least 3 feature cards.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()
    print("Verification complete.")

if __name__ == "__main__":
    run()
