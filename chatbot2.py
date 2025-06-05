import os
import streamlit as st
from openai import OpenAI
API_KEY = ""
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=API_KEY,
)

st.set_page_config(page_title="Chat with GPT-4o", page_icon="🤖")
st.title("Chat with GPT-4o")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system message
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")

# User input
user_input = st.text_input("Enter your question:")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o",
                messages=st.session_state.messages,
                temperature=1,
                max_tokens=4096,
                top_p=1,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")