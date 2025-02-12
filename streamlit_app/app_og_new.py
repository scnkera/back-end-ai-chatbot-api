# from langchain.document_loaders import JSONLoader
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader, PyPDFLoader, DirectoryLoader, TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests

# streamlit
import streamlit as st

# watchon ai ibm
from wxai_langchain.llm import LangChainInterface, Credentials
from langchain_community.llms.utils import enforce_stop_tokens

from datetime import datetime

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



user_id = 1
character_id = 1

# API URLs
history_url = f"http://127.0.0.1:8000/bot_app/conversation/{user_id}/{character_id}/"
save_url = f"http://127.0.0.1:8000/bot_app/conversation/{user_id}/{character_id}/save/"

# Streamlit UI
st.title("Chat with Barack Obama")

# Fetch conversation history
response = requests.get(history_url)

# if response.status_code == 200:
#     history = response.json()
#     st.subheader("Conversation History")
#     for entry in history:
#         st.write(f"**You:** {entry['user_input']}")
#         st.write(f"**{entry['response']}**")
#         st.write(f"*Time: {entry['created_at']}*\n")
# else:
#     st.write("No conversation history found.")

if response.status_code == 200:
    history = response.json()
    st.subheader("Conversation History")
    for entry in history:
        # Convert and format the datetime
        created_at_str = entry['created_at']
        created_at_obj = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        formatted_time = created_at_obj.strftime('%B %d, %Y at %I:%M %p UTC')
        
        # Display conversation history with formatted time
        st.write(f"**You:** {entry['user_input']}")
        st.markdown(f"<p style='font-style: italic;'>*Time: {formatted_time}*</p>", unsafe_allow_html=True)
        st.write(f"**{entry['response']}**")
        st.markdown(f"<p style='text-align: right; font-style: italic;'>*Time: {formatted_time}*</p>", unsafe_allow_html=True)
else:
    st.write("No conversation history found.")

# User Input
user_input = st.text_input("Your message:")

if user_input:
    # Get AI response from Watson API
    bot_response = llm(user_input)

    # Display user input and bot response
    st.write(f"**You:** {user_input}")
    st.write(f"**{bot_response}**")

    # Save the conversation in the database
    payload = {"user_input": user_input, "bot_response": bot_response}
    save_response = requests.post(save_url, json=payload)

    st.write(f"Status Code: {save_response.status_code}")  # Debugging
    st.write(f"Response Content: {save_response.text}") 

    if save_response.status_code == 201:
        st.success("Message saved!")
    else:
        st.error("Failed to save message.")