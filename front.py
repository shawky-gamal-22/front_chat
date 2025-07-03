import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Groq Chat", page_icon="🤖", layout="centered")
st.title("🤖 Chat with Groq LLM (Non-Streaming)")

# Initialize session state for session_id and chat history
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # Unique session ID

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display current session ID in the sidebar
with st.sidebar:
    st.markdown("### Current Session ID")
    st.code(st.session_state.session_id)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI endpoint
    response = requests.post(
        "https://ai-team-chatpot-production.up.railway.app/chat",
        json={"message": prompt, "session_id": st.session_state.session_id}
    )

    response_dict = response.json()
    assistant_reply = response_dict.get("response", "")

    # Display assistant reply
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    # Append assistant reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
