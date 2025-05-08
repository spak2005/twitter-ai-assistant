import streamlit as st
import re
import random
from collections import Counter
from scraper import scrape_tweets
from qa import ask_question

st.set_page_config(
    page_title="Twitter AI Feed Assistant", 
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Twitter AI Feed Assistant")
st.markdown("Scrape your Twitter feed and ask questions about what you saw today.")

# Initialize session state
if "tweets" not in st.session_state:
    st.session_state.tweets = []
    
# Add a function to clean and filter tweets
def filter_tweets(tweets, min_length=0, max_length=10000, keyword=None):
    filtered = []
    for tweet in tweets:
        if min_length <= len(tweet) <= max_length:
            if keyword is None or keyword.lower() in tweet.lower():
                filtered.append(tweet)
    return filtered

scrape_duration = st.slider("Scrape duration (seconds)", 60, 300, 120)

if "is_scraping" not in st.session_state:
    st.session_state.is_scraping = False
    
if "streamed_tweets" not in st.session_state:
    st.session_state.streamed_tweets = []

if st.button(f"🧹 Scrape Feed ({scrape_duration} secs)"):
    st.session_state.is_scraping = True
    st.session_state.streamed_tweets = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    live_tweets = st.empty()
    
    def update_progress(current_time, total_time, tweet_count, new_tweet=None):
        progress = min(current_time / total_time, 1.0)
        progress_bar.progress(progress)
        status_text.text(f"Scrolling... {tweet_count} tweets found ({int(progress*100)}%)")
        
        # If we have a new tweet, add it to the streamed tweets
        if new_tweet and new_tweet not in st.session_state.streamed_tweets:
            st.session_state.streamed_tweets.insert(0, new_tweet)  # Add to beginning
            # Keep only recent tweets in the stream view
            if len(st.session_state.streamed_tweets) > 10:
                st.session_state.streamed_tweets = st.session_state.streamed_tweets[:10]
                
            # Display live stream of tweets
            tweet_html = "<div style='height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; border-radius: 5px;'>"
            for i, tweet_text in enumerate(st.session_state.streamed_tweets):
                # Limit tweet display length and add some styling
                short_tweet = tweet_text[:120] + ("..." if len(tweet_text) > 120 else "")
                tweet_html += f"<div style='margin-bottom: 10px; padding: 8px; background-color: #f9f9f9; border-radius: 4px;'>{short_tweet}</div>"
            tweet_html += "</div>"
            live_tweets.markdown(tweet_html, unsafe_allow_html=True)
    
    with st.spinner("Connecting to Twitter..."):
        st.session_state.tweets = scrape_tweets(duration=scrape_duration, progress_callback=update_progress)
    
    progress_bar.progress(1.0)
    st.session_state.is_scraping = False
    st.success(f"Scraped {len(st.session_state.tweets)} tweets!")
    
    # Show stats of collected tweets
    if len(st.session_state.tweets) > 0:
        st.write(f"📊 Total Tweets Collected: **{len(st.session_state.tweets)}**")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Most Common Words", expanded=True):
                # Simple word frequency analysis
                from collections import Counter
                import re
                
                all_text = " ".join(st.session_state.tweets)
                words = re.findall(r'\b\w+\b', all_text.lower())
                common_words = Counter(words).most_common(10)
                for word, count in common_words:
                    if len(word) > 3:  # Skip short words
                        st.write(f"**{word}**: {count} times")
        
        with col2:
            with st.expander("Sample Tweets", expanded=True):
                for i, tweet in enumerate(st.session_state.tweets[:5]):
                    st.text(f"Tweet {i+1}: {tweet[:100]}..." if len(tweet) > 100 else f"Tweet {i+1}: {tweet}")


if st.session_state.tweets:
    # Tweet analysis section
    st.header("📊 Tweet Analysis")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_length = st.slider("Min tweet length", 0, 500, 20)
    with col2:
        max_length = st.slider("Max tweet length", 100, 1000, 500)
    with col3:
        keyword_filter = st.text_input("Filter by keyword:", "")
    
    # Apply filters
    filtered_tweets = filter_tweets(
        st.session_state.tweets,
        min_length=min_length,
        max_length=max_length,
        keyword=keyword_filter if keyword_filter else None
    )
    
    st.write(f"Showing {len(filtered_tweets)} of {len(st.session_state.tweets)} tweets")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Ask AI", "Tweet Explorer", "Statistics"])
    
    with tab1:
        # AI question answering
        st.subheader("Ask about your Twitter feed")
        question = st.text_input("Ask something about today's feed:", "")
        if question:
            with st.spinner("Thinking..."):
                answer = ask_question(filtered_tweets, question)
                st.markdown(f"**Answer:** {answer}")
                
                # Example questions
                st.markdown("### Try asking:")
                example_questions = [
                    "What are the main topics people are discussing?",
                    "What's the most controversial topic in my feed?",
                    "Summarize the key news stories in my feed",
                    "What's trending in tech right now?",
                    "Who are the most mentioned people?"
                ]
                for q in example_questions:
                    st.markdown(f"- {q}")
    
    with tab2:
        # Show random samples of tweets in a scrollable container
        st.subheader("Sample of collected tweets")
        
        tweet_sample = random.sample(filtered_tweets, min(10, len(filtered_tweets)))
        for i, tweet in enumerate(tweet_sample):
            st.text_area(f"Tweet {i+1}", tweet, height=100)
            st.markdown("---")
    
    with tab3:
        # Word frequency analysis
        st.subheader("Common Words")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Word cloud would be nice but requires additional dependencies
            all_text = " ".join(filtered_tweets)
            words = re.findall(r'\b\w+\b', all_text.lower())
            word_freq = Counter(words)
            
            # Filter out common words
            stopwords = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'on', 'with', 'as', 'this', 'that', 'are', 'at'}
            for word in stopwords:
                if word in word_freq:
                    del word_freq[word]
            
            common_words = word_freq.most_common(15)
            for word, count in common_words:
                if len(word) > 3:  # Skip short words
                    st.write(f"**{word}**: {count} times")
        
        with col2:
            # Tweet length distribution
            tweet_lengths = [len(tweet) for tweet in filtered_tweets]
            avg_length = sum(tweet_lengths) / len(filtered_tweets) if filtered_tweets else 0
            st.write(f"Average tweet length: **{avg_length:.1f}** characters")
            st.write(f"Shortest tweet: **{min(tweet_lengths)}** characters")
            st.write(f"Longest tweet: **{max(tweet_lengths)}** characters")
            
            # Count mentions and hashtags
            mentions = re.findall(r'@\w+', all_text.lower())
            hashtags = re.findall(r'#\w+', all_text.lower())
            
            st.write(f"Total mentions: **{len(mentions)}**")
            st.write(f"Total hashtags: **{len(hashtags)}**")
            
            # Most common mentions
            if mentions:
                st.write("**Top mentions:**")
                for mention, count in Counter(mentions).most_common(5):
                    st.write(f"{mention}: {count} times")
