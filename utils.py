import streamlit as st
from datetime import datetime
import tiktoken
from fpdf import FPDF



def get_time():
    """return time"""
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def get_open_ai_key():
    """get openai key
    :return:
    """
    return st.secrets["OPENAI_API_KEY"]


def get_tokens(text: str, model_name: str) -> int:
    """
    calculate the number of tokens corresponding to text and tokenizer for that model
    :param model_name:
    :param text:
    :return:
    """
    tokenizer = tiktoken.encoding_for_model(model_name)
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)


def get_pdf(log_file) -> str:
    """
    convert text file as pdf
    :param log_file:
    :return:
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    f = log_file
    for x in f.split("\n"):
        pdf.multi_cell(0, 5, x)
    fout = "app.pdf"
    pdf.output(fout)
    return fout


def template_insurance():
    """
    :return: prompt template
    """
    # template = """let's play a game where you ask me a series of questions, the order of which is influenced by my responses. every time I say "new game" we restart the process.
    #
    #     the first question is "what is your name?"
    #
    #     After that, ask for my height and weight then calculate my BMI.
    #     If it is greater than 35, then ask for my average weight for the last 3 years.
    #     if it is less than 35, move forward to the next question.
    #
    #     The next question is "Are you currently taking any medications?"
    #
    #     If I say yes, ask for the medications and dosages.
    #     If I give you more than 2 medications, also ask me to list the reasons i'm taking those medicines.
    #     If I say I take no medicines, move on to the next question.
    #
    #     The next question is whether I currently have any diseases.
    #     If I say no, the game is over.
    #     Write a summary of my answers as a bullet point list.
    #
    #     if I say yes, ask me if I have any metabolic and/or cardiovascular diseases.
    #     if I say yes to metabolic, ask me if I have diabetes or obesity.
    #     if I say yes to cardiovascular diseases, ask me what my cholesterol and blood pressure are.
    #
    #     This ends the game. Write a summary of my answers as bullet point list.
    # """

    template = """let's play a game where you ask me a series of questions, the order of which is influenced by my responses. every time I say "new game" we restart the process. 

            the first question is "what is your name?" 

            After that, ask for my height in centimeters and weight in pounds then calculate my BMI. Do not give the calculations details.
            If it is greater than 35, then ask for my average weight for the last 3 years. 
            if it is less than 35, move forward to the next question.

            The next question is "Are you currently taking any medications?" 

            If I say yes, ask for the medications and dosages. 
            If I give you more than 2 medications, also ask me to list the reasons i'm taking those medicines. 
            If I say no, move on to the next question.

            The next question is whether I currently have any diseases. 
            
            If I say no, move on the next question.
            if I say yes, ask me if I have any metabolic or cardiovascular diseases. 
            if I say yes to metabolic, ask me if I have diabetes or obesity. 
            if I say yes to cardiovascular diseases, ask me what my cholesterol and blood pressure are.
            Then move on the next question.
            
            The next question is about my life style. Ask me if I have been out of country in last 3 years ?
            If I say yes, then ask about the locations and dates for each of them then move on the next question.
            If I say no, move on the next question.
            
            The next question is "Do you have any hobbies or sports or activities ?"
            If I say yes, ask for the frequency for each of them? This ends the game.
            If I say no, this ends the game.

            Game is over: summarize my answers. Use a bullet list.
        """
    return template
