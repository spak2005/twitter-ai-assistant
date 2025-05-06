import streamlit as st
from scraper import scrape_tweets
from qa import ask_question

st.title("🧠 Twitter AI Feed Assistant")
st.markdown("Scrape your Twitter feed and ask questions about what you saw today.")

if "tweets" not in st.session_state:
    st.session_state.tweets = []

if st.button("🧹 Scrape Feed (2 mins)"):
    with st.spinner("Scrolling through Twitter..."):
        st.session_state.tweets = scrape_tweets(duration=120)
    st.success(f"Scraped {len(st.session_state.tweets)} tweets!")

if st.session_state.tweets:
    question = st.text_input("Ask something about today's feed:", "")
    if question:
        with st.spinner("Thinking..."):
            answer = ask_question(st.session_state.tweets, question)
            st.markdown(f"**Answer:** {answer}")
