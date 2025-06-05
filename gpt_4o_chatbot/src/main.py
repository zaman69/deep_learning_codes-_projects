"""
⚠️ Why This App Doesn't Show GPT Responses

# This chatbot uses the OpenAI API (GPT-4o model), which requires an active API key and valid billing. However:

# - The API key used in this app is currently on the free tier.
# - Free tier credits have likely expired or been fully used.
# - Since I don't have a credit card, I cannot add billing information to continue using the API.

# Therefore, the chatbot interface loads correctly, but any message sent returns the following message:

# > ⚠️ You've exceeded your OpenAI quota or rate limit.

# Once an API key with billing access is added, the chatbot will work as expected.
"""








import os
import json
import streamlit as st
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

# 1️⃣ Load OpenAI API key from config.json
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")

try:
    with open(config_path, "r") as f:
        config_data = json.load(f)
        OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
except Exception as e:
    st.error(f"⚠️ Error loading API key: {e}")
    st.stop()

# 2️⃣ Create OpenAI client using your API key
client = OpenAI(api_key=OPENAI_API_KEY)

# 3️⃣ Streamlit page setup
st.set_page_config(
    page_title="GPT-4O Chat by ZAMAN",
    page_icon="💬",
    layout="centered"
)

st.title("🧠 GPT-4O - CHATBOT, CREATED BY ZAMAN")

# 4️⃣ Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5️⃣ Show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6️⃣ Take user input
user_prompt = st.chat_input("Ask GPT-4O...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # 7️⃣ Get response from GPT-4O with error handling
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *st.session_state.chat_history
            ]
        )
        assistant_response = response.choices[0].message.content

    except RateLimitError:
        assistant_response = "⚠️ You've exceeded your OpenAI quota or rate limit. Check: [OpenAI Usage](https://platform.openai.com/account/usage)"
    except AuthenticationError:
        assistant_response = "⚠️ API Key error: Your API key is missing or invalid. Please check your config.json."
    except APIError as e:
        assistant_response = f"⚠️ OpenAI API error: {e}"
    except Exception as e:
        assistant_response = f"⚠️ An unexpected error occurred: {e}"

    # 8️⃣ Show GPT's reply
    st.chat_message("assistant").markdown(assistant_response)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
