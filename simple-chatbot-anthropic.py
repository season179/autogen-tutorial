import os
import streamlit as st
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Configure the AI assistant
config_list = [
    {
        "model": "claude-3-5-sonnet-20240620",
        "api_key": os.environ["ANTHROPIC_API_KEY"],
        "api_type": "anthropic",
    }
]

assistant = AssistantAgent(
    name="AI Assistant",
    llm_config={
        "config_list": config_list,
    },
)

user_proxy = UserProxyAgent(
    name="Human", human_input_mode="NEVER", max_consecutive_auto_reply=0
)

# Streamlit app
st.title("Autogen Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response
    user_proxy.initiate_chat(assistant, message=prompt)

    # Extract the response from the user_proxy's last message
    response_content = user_proxy.last_message()["content"]

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_content)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})

    # Optionally, display additional information about the response
    with st.expander("View Chat History"):
        st.json(assistant.chat_messages[user_proxy])
