import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_question(tweets, question):
    tweets_text = "\n\n".join(tweets[:50])  # Limit to recent ones
    prompt = f"These are tweets I saw today:\n\n{tweets_text}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4-turbo" or "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
