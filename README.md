# streamlit_base_demo_chatbot

- demo for chatbot using `openai` and `streamlit`
- features:
  - `openai` api key 
  - dropdown menu to choose model
  - selectbox to output the number of tokens
  - possibility to download the transcript at any time

LLM model is using:
- `ConversationBufferWindowMemory` with k = 10
- initial prompt