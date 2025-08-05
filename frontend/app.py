import streamlit as st
import os
import requests
import uuid
import sys
from loguru import logger


APP_NAME = "m-5-brief-0"
M_5_BRIEF_0_FRONTEND_API_URL = os.getenv("M_5_BRIEF_0_FRONTEND_API_URL", "http://127.0.0.1:9000")


# Logs

logger.remove()
logger.add(sys.stdout, level="INFO", format="[{time}] {level} - {message}")
M_5_BRIEF_0_FRONTEND_LOG_PATH = os.getenv("M_5_BRIEF_0_FRONTEND_LOG_PATH")
if M_5_BRIEF_0_FRONTEND_LOG_PATH:
    logger.add(f"{M_5_BRIEF_0_FRONTEND_LOG_PATH}", rotation="1 week", retention="4 weeks", level="INFO", format="[{time}] {level} - {message}")


def get_calculation(n, language=None):

    response = requests.get(f"{M_5_BRIEF_0_FRONTEND_API_URL}/calculation", params={"n": n})
    data = response.json()
    res = data["results"]
    return res


def main():

    session_id = str(uuid.uuid4())

    logger.info(f"{session_id} Loading page...")

    # Session management
    if "session_uid" not in st.session_state:
        st.session_state.session_uid = str()
    # Store messages in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Set page configuration
    st.set_page_config(page_title=APP_NAME, page_icon="💬")

    # Title
    st.title(f"💬 {APP_NAME}")

    # Display chat messages from history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    logger.info(f"{session_id} Processing chat messages...")
                
    # Prompt for user input
    if prompt := st.chat_input("Give a number..."):
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        logger.info(f"{session_id} Calculation for user input...")
        res = get_calculation(prompt)
        st.session_state.messages.append({"role": "assistant", "content": res})

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(res)

main()
