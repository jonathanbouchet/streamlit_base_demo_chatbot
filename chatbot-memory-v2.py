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
from PIL import Image
from datetime import datetime


def add_logo(logo_path):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    return logo


def get_open_ai_key():
    """
    get openai key
    :return:
    """
    return st.secrets["OPENAI_API_KEY"]


def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses']) - 1):
        conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: " + st.session_state['responses'][i + 1] + "\n"
    return conversation_string


def query_refiner(conversation, query):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']


openai_api_key = get_open_ai_key()

st.title("Reflexive AI")
st.header("Virtual Insurance Agent")
my_logo = add_logo(logo_path="./Reflexive.jpg")
st.sidebar.image(my_logo)

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

llm = ChatOpenAI(model_name=MODEL, openai_api_key=openai_api_key, temperature=0)

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory=ConversationBufferWindowMemory(
        k=10,
        return_messages=True
    )

template_insurance="""let's play a game where you ask me a series of questions, the order of which is influenced by my responses. every time I say "new game" we restart the process. 
    If you do not know the answer to a question, you truthfully says it.
    The first question is "what is your name?" 
    The next question is "what is your gender?"
    After that, ask for my height in centimeters and weight in pounds. 
    The next step for you is to calculate my body mass index (BMI). 
    If it is greater than 35, then you ask for my average weight for the last 3 years, otherwise move forward to the next step.
    The next step is determine if I am underweight, healthy or overweight, based on my gender and BMI.
    The next step is to end the game by presenting me with a summary of my answer in a bulleted list format.
    """


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

# system_msg_template = SystemMessagePromptTemplate.from_template(
#     template="""Answer the question as truthfully as possible using the provided context,
# and if the answer is not contained within the text below, say 'I don't know'"""
# )
system_msg_template = SystemMessagePromptTemplate.from_template(
    template=template_insurance
)

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
prompt_template = ChatPromptTemplate.from_messages(
    [system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template]
)
conversation = ConversationChain(
    memory=st.session_state.buffer_memory,
    prompt=prompt_template,
    llm=llm, verbose=True
)

# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

download_str = []
with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        print(f"query:{query}")
        download_str.append(query)
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            # st.code(conversation_string)
            # refined_query = query_refiner(conversation_string, query)
            st.subheader("Query:")
            st.write(query)
            # context = find_match(refined_query)
            # print(context)
            response = conversation.predict(input=f"Query:\n{query}")
            download_str.append(query)
            download_str.append(response)
            print(f"current transcript:{download_str}")

            # Can throw error - requires fix
            # download_str_current = '\n'.join(download_str)
            # if download_str_current:
            #     print(f"current date:{datetime.now()}")
            #     now = datetime.now()
            #     st.download_button(
            #         label="Download data as CSV",
            #         data=download_str_current,
            #         file_name=f"reflexive.ai-virtual-assistant-{now.strftime('%d-%m-%Y-%H-%M-%S')}.csv",
            #         mime="text/csv")

        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
        # download_str.append(query)
        # download_str.append(response)
        # print(download_str)

with response_container:
    if st.session_state['responses']:
        # print(f"current transcript:{download_str}")

        # Can throw error - requires fix
        download_str_current = '\n'.join(download_str)
        if download_str_current:
            print(f"current date:{datetime.now()}")
            now = datetime.now()
            st.download_button(
                label="Download data as CSV",
                data=download_str_current,
                file_name=f"reflexive.ai-virtual-assistant-{now.strftime('%d-%m-%Y-%H-%M-%S')}.csv",
                mime="text/csv")

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],
                    key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i],
                        is_user=True,
                        key=str(i) + '_user')
