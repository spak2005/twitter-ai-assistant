from playwright.sync_api import sync_playwright
import time

def scrape_tweets(duration=120):  # seconds
    tweets = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Log in first time manually and stay logged in
        page.goto("https://twitter.com/home")
        time.sleep(60)  # Give time to login manually

        # Scroll and collect tweets
        start = time.time()
        while time.time() - start < duration:
            page.mouse.wheel(0, 1000)
            time.sleep(1)

        tweet_elements = page.query_selector_all("article div[lang]")

        for tweet in tweet_elements:
            text = tweet.inner_text()
            tweets.append(text)

        browser.close()

    return tweets
