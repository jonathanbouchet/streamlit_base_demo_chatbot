# streamlit_base_demo_chatbot

- update: `2023-07-24`
  - added downlad as pdf
  - add life style question in prompt

This is a features branch for experiments

- demo for chatbot using `openai` and `streamlit`
- features:
  - `openai` api key 
  - dropdown menu to choose model
  - selectbox to output the number of tokens
  - possibility to download the transcript at any time

LLM model is using:
- `ConversationBufferWindowMemory` with k = 10
- initial prompt