from playwright.sync_api import sync_playwright
import time

def scrape_tweets(duration=120, progress_callback=None):  # seconds
    tweets = []
    seen_tweets = set()  # For more efficient duplicate checking

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to Twitter (assumes you're already logged in)
        page.goto("https://twitter.com/home")
        print("Please ensure you're logged in... waiting 10s")
        time.sleep(10)  # Reduced login time

        start = time.time()
        last_tweet_count = 0
        
        # For streaming UI - store the last few tweets we've seen
        recently_processed = []
        
        while time.time() - start < duration:
            current_time = time.time() - start
            
            # Collect tweets continuously during scrolling
            tweet_elements = page.query_selector_all("article")
            
            new_tweet_found = False
            newest_tweet = None
            
            for tweet in tweet_elements:
                try:
                    text = tweet.inner_text()
                    # Use a hash-based approach to check for duplicates
                    text_hash = hash(text)
                    if text.strip() and text_hash not in seen_tweets and len(text) > 20:  # Ignore very short texts
                        tweets.append(text)
                        seen_tweets.add(text_hash)
                        new_tweet_found = True
                        newest_tweet = text
                        
                        # Keep track of recent tweets for streaming display
                        if len(recently_processed) >= 5:
                            recently_processed.pop(0)  # Remove oldest
                        recently_processed.append(text)
                except:
                    pass
            
            # If we found new tweets, log progress
            if len(tweets) > last_tweet_count:
                print(f"Found {len(tweets) - last_tweet_count} new tweets. Total: {len(tweets)}")
                last_tweet_count = len(tweets)
            
            # Update progress if callback provided
            if progress_callback:
                # Pass the newest tweet for streaming display
                if new_tweet_found and newest_tweet:
                    progress_callback(current_time, duration, len(tweets), new_tweet=newest_tweet)
                else:
                    progress_callback(current_time, duration, len(tweets))
            
            # Scroll faster and try different scroll amounts to avoid Twitter's scroll detection
            if len(tweets) % 5 == 0:
                page.mouse.wheel(0, 2000)  # Occasionally scroll more
            else:
                page.mouse.wheel(0, 1200)
            
            # Variable wait time
            time.sleep(0.8)  # Faster scrolling but still allow content to load

        print(f"✅ Scraped {len(tweets)} tweets.")
        browser.close()

    return tweets
