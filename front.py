import streamlit as st
import requests
import uuid
from typing import Optional

# Page config
st.set_page_config(
    page_title="Rafeq Chat",
    page_icon="💬",
    layout="centered"
)

# Custom CSS for chat bubbles and improved contrast
st.markdown("""
    <style>
    body {
        background-color: #181a1b;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 0.7rem;
        margin-bottom: 1.2rem;
        display: flex;
        flex-direction: column;
        font-size: 1.1rem;
    }
    .chat-message.user {
        background-color: #e3e3e3;
        color: #181a1b;
        border: 1px solid #bdbdbd;
    }
    .chat-message.bot {
        background-color: #23272f;
        color: #f5f5f5;
        border: 1px solid #444857;
    }
    .chat-message .avatar {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        margin-right: 0.7rem;
        display: inline-block;
        vertical-align: middle;
    }
    .chat-message .name {
        font-weight: bold;
        margin-right: 0.5rem;
        display: inline-block;
        vertical-align: middle;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Header
st.title("💬 Rafeq Chat")
st.markdown("Welcome! I'm Rafeq, your AI assistant. How can I help you today?")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This is a chat interface powered by Phi-4 model.
    The conversation history is maintained during your session.
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Chat input
user_input = st.text_input(
    "Type your message here...",
    key=f"user_input_{st.session_state.input_key}",
    placeholder="Ask me anything..."
)

# Send button
send_button = st.button("Send", type="primary")

def display_message(speaker: str, text: str):
    if speaker == "User":
        st.markdown(f"""
            <div class="chat-message user">
                <span class="avatar">🧑</span>
                <span class="name">You:</span>
                <span>{text}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message bot">
                <span class="avatar">🤖</span>
                <span class="name">Rafeq:</span>
                <span>{text}</span>
            </div>
        """, unsafe_allow_html=True)

# Handle message sending
if (send_button or user_input) and user_input.strip() != "":
    # Get response from API
    response = requests.post(
        "https://ai-team-chatpot-production.up.railway.app/chat",
        json={
            "message": user_input,
            "session_id": st.session_state.session_id
        },
        headers={"X-Session-ID": st.session_state.session_id}
    )
    
    # Extract response
    response_data = response.json()
    bot_reply = response_data.get("response", "No reply")
    
    # Update session ID if it changed
    if "session_id" in response_data:
        st.session_state.session_id = response_data["session_id"]
    
    # Save conversation history
    st.session_state.chat_history.append(("User", user_input))
    st.session_state.chat_history.append(("Bot", bot_reply))
    
    # Clear input by incrementing the input key
    st.session_state.input_key += 1
    st.rerun()

# Display chat history
for speaker, text in st.session_state.chat_history:
    display_message(speaker, text)

# Add some space at the bottom
st.markdown("<br>" * 2, unsafe_allow_html=True)
