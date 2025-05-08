import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Try to load from .env file first
load_dotenv()

# Function to get API key either from environment or from Streamlit secrets
def get_api_key():
    # First try environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    
    # If not found in environment, try Streamlit secrets
    if not api_key and hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
        api_key = st.secrets['OPENAI_API_KEY']
        
    return api_key

# Create client with the API key
def create_client():
    api_key = get_api_key()
    if api_key:
        return OpenAI(api_key=api_key)
    else:
        st.error("OpenAI API key not found. Please add it to your .env file or Streamlit secrets.")
        return None

def ask_question(tweets, question):
    client = create_client()
    if not client:
        return "Error: OpenAI API key not configured. Please check configuration."
    
    tweets_text = "\n\n".join(tweets[:50])  # Limit to recent ones
    prompt = f"These are tweets I saw today:\n\n{tweets_text}\n\nQuestion: {question}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4-turbo" or "gpt-3.5-turbo"
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"
