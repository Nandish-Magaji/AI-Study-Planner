from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

@st.cache_resource
def load_model(model_name):
    return ChatGroq(
    model=model_name,
    groq_api_key=st.secrets["GROQ_API_KEY"]
)

def generate_response(prompt, model_name):
    model = load_model(model_name)
    parser = StrOutputParser()
    chain = model | parser
    return chain.invoke(prompt)
