# from langchain.document_loaders import JSONLoader
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader, PyPDFLoader, DirectoryLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# streamlit
import streamlit as st

# watchon ai ibm
from wxai_langchain.llm import LangChainInterface, Credentials
from langchain_community.llms.utils import enforce_stop_tokens

from datetime import datetime
import requests
import pytz

load_dotenv()

# llm configurations
credentials = Credentials(
    api_key=os.environ.get('WATSON_API_KEY'),
    project_id=os.environ.get('WATSON_PROJECT_ID'),
    api_endpoint=os.environ.get('WATSON_URL')
)

parameters = {
    'decoding_method': 'sample',
    'min_new_tokens': 1,
    'max_new_tokens': 200,
    'temperature': 0.5
}

llm = LangChainInterface(
    credentials=credentials,
    model='meta-llama/llama-2-13b-chat',
    params=parameters
)

# # training data

# @st.cache_resource
# def load_pdf():
#     json_name = "barack_obama.json"
#     loaders = [JSONLoader(json_name)]

#     index = VectorstoreIndexCreator(
#         embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
#         text_splitter=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
#     ).from_loaders(loaders)
#     return index

# index = load_pdf()

# chain = RetrievalQA.from_chain_type(
#     LLm=llm,
#     chain_type='stuff',
#     retriever=index.vectorestore.as_retriever(),
#     input_key='question'
#     )

# Streamlit setup
st.title('Chat with Barack Obama')

# API URLs for conversation history
user_id = 1
character_id = 1
history_url = f"http://127.0.0.1:8000/bot_app/conversation/{user_id}/{character_id}/"
save_url = f"http://127.0.0.1:8000/bot_app/conversation/{user_id}/{character_id}/save/"

# Fetch conversation history
response = requests.get(history_url)

if response.status_code == 200:
    history = response.json()
    est = pytz.timezone('America/New_York')

    for entry in history:
        # Convert and format the datetime
        created_at_str = entry['created_at']
        created_at_obj = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        created_at_est = created_at_obj.astimezone(est)
        
        # Format time in EST
        formatted_time = created_at_est.strftime('%B %d, %Y at %I:%M %p')
        
        # Display conversation history with formatted time


        # st.chat_message('user').markdown(f"""<div style='text-align: right; padding: 10px; border-radius: 10px; width: fit-content; margin-left: auto;'>
        #     <strong>You:</strong> {entry['user_input']}</div>
        # """, unsafe_allow_html=True)


        # st.markdown(f"""<div style='text-align: right; padding: 10px; background-color: #1E2029; border-radius: 10px; width: fit-content; margin-left: auto;'>
        #     <strong>You:</strong> {entry['user_input']}</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style='text-align: right; padding: 10px; border: 1px solid #666970; background-color: #21242E; border-radius: 10px; width: fit-content; margin-left: auto;'>
            <img src='https://i.pinimg.com/1200x/35/99/27/359927d1398df943a13c227ae0468357.jpg' alt='Image' style='width: 25px; height: 25px; border-radius: 5px;'>
            <strong>&nbsp;&nbsp;&nbsp;You:&nbsp;</strong> {entry['user_input']}</div>""", unsafe_allow_html=True)

        st.markdown(f"<p style='text-align: right; font-style: italic;'>*Delivered: {formatted_time}*</p>", unsafe_allow_html=True)
        
        st.chat_message('assistant').markdown(f"**{entry['response']}**")
else:
    st.write("No conversation history found.")

# Initialize conversation state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display conversation history in chat format
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# User Input
prompt = st.chat_input('Write to Me')

if prompt:
    # st.chat_message('user').markdown(prompt)
    # st.session_state.messages.append({'role': 'user', 'content': prompt})
    # st.markdown(f"""<div style='text-align: right; padding: 10px; background-color: #1A1C24; border-radius: 10px; width: fit-content; margin-left: auto;'>
    # <strong>You:</strong> {prompt}</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style='text-align: right; padding: 10px; border: 1px solid #666970; background-color: #21242E; border-radius: 10px; width: fit-content; margin-left: auto;'>
    <img src='https://i.pinimg.com/1200x/35/99/27/359927d1398df943a13c227ae0468357.jpg' alt='Image' style='width: 25px; height: 25px; border-radius: 5px;'>
    <strong>&nbsp;&nbsp;&nbsp;You:&nbsp;</strong> {prompt}</div>""", unsafe_allow_html=True)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Get AI response from Watson API
    response = llm(prompt)

    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})

    # Save the conversation in the database
    payload = {"user_input": prompt, "bot_response": response}
    save_response = requests.post(save_url, json=payload)

    # st.write(f"Status Code: {save_response.status_code}")  # Debugging
    # st.write(f"Response Content: {save_response.text}") 

    if save_response.status_code != 201:
        st.error("Failed to save message.")
