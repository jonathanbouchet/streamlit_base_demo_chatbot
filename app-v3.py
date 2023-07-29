import streamlit as st
import sys
sys.path.insert(1, './pyttsx3')
import pyttsx3

st.title("Reflexive AI")
st.header("Virtual Insurance Agent")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
                st.session_state["username"] in st.secrets["passwords"]
                and st.session_state["password"]
                == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        print("password_correct not in st.session_state")
        # First run, show inputs for username + password.
        st.sidebar.text_input("Username", on_change=password_entered, key="username", placeholder="user123")
        st.sidebar.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        print("Password not correct, show input + error.")
        # Password not correct, show input + error.
        st.sidebar.text_input("Username", on_change=password_entered, key="username", placeholder="user123")
        st.sidebar.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    # Set API key
    openai_api_key = st.sidebar.text_input(
        ":blue[API-KEY]",
        placeholder="Paste your OpenAI API key here",
        type="password")

    MODEL = st.sidebar.selectbox(
        label=":blue[MODEL]",
        options=["gpt-3.5-turbo-16k-0613",
                 "gpt-3.5-turbo",
                 "gpt-3.5-turbo-16k",
                 "gpt-3.5-turbo-0613",
                 "text-davinci-003",
                 "text-davinci-002"])

    show_tokens = st.sidebar.radio(label=":blue[Display tokens]", options=('Yes', 'No'))

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    # print(f"start : st.session_state: {st.session_state.messages}, size: {len(st.session_state.messages)}")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    # print(f"before user input : st.session_state: {st.session_state.messages}, size: {len(st.session_state.messages)}")
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # print(f"before assistant answer : st.session_state: {st.session_state.messages}, size: {len(st.session_state.messages)}")
        response = f"Echo: {prompt}"
        # print(response)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        print("here")
        engine = pyttsx3.init()
        engine.say(prompt)
        engine.runAndWait()
        engine = None
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
