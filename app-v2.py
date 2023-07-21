import logging
from io import StringIO

import openai
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from datetime import datetime

# Current log value
log_stream = StringIO()

# Create and configure logger
# logging.basicConfig(
#     filename="app.log",
#     format='%(asctime)s %(message)s',
#     filemode='w',)

logging.basicConfig(format='%(asctime)s %(message)s', stream=log_stream, level=logging.INFO)

# Creating an object
# logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
# logger.setLevel(logging.INFO)


def get_time():
    """return time"""
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def get_open_ai_key():
    """get openai key
    :return:
    """
    return st.secrets["OPENAI_API_KEY"]


def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses']) - 1):
        conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: " + st.session_state['responses'][i + 1] + "\n"
    return conversation_string


# openai_api_key = get_open_ai_key()

# Set API key
openai_api_key = st.sidebar.text_input(
    ":blue[API-KEY]",
    placeholder="Paste your OpenAI API key here",
    type="password")

st.title("Reflexive AI")
st.header("Virtual Insurance Agent")

MODEL = st.sidebar.selectbox(
    label=":blue[MODEL]",
    options=["gpt-3.5-turbo-16k-0613",
             "gpt-3.5-turbo",
             "gpt-3.5-turbo-16k",
             "gpt-3.5-turbo-0613",
             "text-davinci-003",
             "text-davinci-002"])

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if openai_api_key:

    # llm = ChatOpenAI(model_name=MODEL, openai_api_key=openai_api_key, temperature=0)

    if 'buffer_memory' not in st.session_state:
        pass
        # st.session_state.buffer_memory=ConversationBufferWindowMemory(
        #     k=10,
        #     return_messages=True
        # )

    template_insurance="""let's play a game where you ask me a series of questions, the order of which is influenced by my responses. every time I say "new game" we restart the process. 
        the first question is "what is your name?" 
        After that, ask for my height and weight then calculate my BMI. 
        If it is greater than 35, then ask for my average weight for the last 3 years. 
        if it is less than 35, move forward to the next question which is "Are you currently taking any medications?" 
        If I say yes, ask for the medications, dosages. 
        If I give you more than 2 medications, also ask me to list the reasons i'm taking those medicines. 
        If I say I take no medicines, move on to the next question which is whether I currently have any diseases. 
        If I say no, the game is over & present a summary of my answers. 
        if I say yes, ask me if I have any metabolic and/or cardiovascular diseases. 
        if I say yes to metabolic, ask me if I have diabetes or obesity. 
        if I say yes to cardiovascular diseases, ask me what my cholesterol and blood pressure are. 
        This ends the game. At the end of the game, present me with a summary of my answers.
    """

    system_msg_template = SystemMessagePromptTemplate.from_template(
        template=template_insurance
    )

    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
    prompt_template = ChatPromptTemplate.from_messages(
        [system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template]
    )
    # conversation = ConversationChain(
    #     memory=st.session_state.buffer_memory,
    #     prompt=prompt_template,
    #     llm=llm, verbose=True
    # )

    # container for chat history
    response_container = st.container()

    # container for text box
    textcontainer = st.container()

    download_str = []
    with textcontainer:
        query = st.text_input("Query: ", key="input")
        if query:
            print(f"query:{query}")
            # download_str.append(f"{get_time()}\tHuman\t{query}")
            with st.spinner("typing..."):
                conversation_string = get_conversation_string()
                st.subheader("Query:")
                st.write(query)
                # response = conversation.predict(input=f"Query:\n{query}")
                response = f"(for debugging only, response = input): {query}"
                download_str.append(f"{get_time()}\tAI\t{response}")
                download_str.append(f"{get_time()}\tHuman\t{query}")
                logging.info(response)
                logging.info(query)
                print(f"current transcript:{download_str}")

            st.session_state.requests.append(query)
            st.session_state.responses.append(response)

    with response_container:
        if st.session_state['responses']:
            download_str_current = '\n'.join(download_str)
            if download_str_current:
                print(f"current date:{datetime.now()}")
                now = datetime.now()
                print(f"log stream:{log_stream.getvalue()}")
                val = log_stream.getvalue()
                st.download_button(
                    label="Download data as CSV",
                    data=val,
                    file_name=f"reflexive.ai-virtual-assistant-{now.strftime('%d-%m-%Y-%H-%M-%S')}.csv",
                    mime="text/csv")

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],
                        key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i],
                            is_user=True,
                            key=str(i) + '_user')
