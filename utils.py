from datetime import datetime
import tiktoken


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


def template_insurance():
    """
    :return: prompt template
    """
    template = """let's play a game where you ask me a series of questions, the order of which is influenced by my responses. every time I say "new game" we restart the process. 
    
        the first question is "what is your name?" 
        
        After that, ask for my height and weight then calculate my BMI. 
        If it is greater than 35, then ask for my average weight for the last 3 years. 
        if it is less than 35, move forward to the next question.
         
        The next question is "Are you currently taking any medications?" 
        
        If I say yes, ask for the medications and dosages. 
        If I give you more than 2 medications, also ask me to list the reasons i'm taking those medicines. 
        If I say I take no medicines, move on to the next question.
        
        The next question is whether I currently have any diseases. 
        If I say no, the game is over.
        Write a summary of my answers as a bullet point list.
        
        if I say yes, ask me if I have any metabolic and/or cardiovascular diseases. 
        if I say yes to metabolic, ask me if I have diabetes or obesity. 
        if I say yes to cardiovascular diseases, ask me what my cholesterol and blood pressure are. 
        
        This ends the game. Write a summary of my answers as bullet point list.
    """
    return template
