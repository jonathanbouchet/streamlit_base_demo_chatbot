import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
import openai
from PIL import Image
from datetime import datetime


def get_open_ai_key():
    """
    get openai key
    :return:
    """
    return st.secrets["OPENAI_API_KEY"]


def add_logo(logo_path):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    return logo

# Initialize streamlit session states


if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.entity_store = {}
    st.session_state.entity_memory.buffer.clear()


def get_text():
    """
    ge tthe user input
    :return:
    """
    input_text = st.text_input(
        "You: ",
        st.session_state["input"],
        key="input",
        placeholder="Your AI agent here. Ask me anything",
        label_visibility="hidden"
    )
    return input_text


st.title("Reflexive.AI")
st.header("Virtual Insurance Agent")
my_logo = add_logo(logo_path="./Reflexive.jpg")
st.sidebar.image(my_logo)

openai_api_key = get_open_ai_key()
MODEL = st.sidebar.selectbox(
    label=":blue[MODEL]",
    options=["gpt-3.5-turbo", "text-davinci-003", "text-davinci-002"])

st.sidebar.button(
    "New Chat",
    on_click=new_chat,
    type='primary')

# Get the user input
user_input = get_text()
if user_input:

    output = user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append(user_input)

    # Allow to download as well
    download_str = []
    # Display the conversation history using an expander, and allow the user to download it
    with st.expander("Conversation", expanded=True):
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            st.info(st.session_state["past"][i], icon="🧐")
            st.success(st.session_state["generated"][i], icon="🤖")
            download_str.append(st.session_state["past"][i])
            download_str.append(st.session_state["generated"][i])

        # Can throw error - requires fix
        download_str = '\n'.join(download_str)
        if download_str:
            now = datetime.now()
            st.download_button(
                label="Download data as CSV",
                data=download_str,
                file_name=f"reflexive.ai-virtual-assistant-{now.strftime('%d-%m-%Y-%H-%M-%S')}.csv",
                mime="text/csv")
