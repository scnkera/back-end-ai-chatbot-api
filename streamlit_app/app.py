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



st.title('Hi, I am Barack Obama')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

prompt = st.chat_input('Write to Me')

if prompt:
    st.chat_message('user').markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = llm(prompt)
    # response = chain.run(prompt)


    # response = response[2:] if response.startswith(", ") else response

    st.chat_message('assistant').markdown(response)

    st.session_state.messages.append(
        {
            'role': 'assistant',
            'content': response
        }
    )