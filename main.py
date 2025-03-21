import tempfile
import os
import logging
from tools import generate_email_from_rag, search, generate_email_from_search, send_email
from langchain import HuggingFaceHub
import streamlit as st

# Initialize the language model
llm = HuggingFaceHub(
    repo_id="google/flan-t5-base", 
    huggingfacehub_api_token=st.secrets["HUGGINGFACE_TOKEN"]
)
sender_email = st.secrets["EMAIL_USER"]
sender_password = st.secrets["EMAIL_PASSWORD"]

def process_and_send_email(recipient_name, recipient_email, email_subject, uploaded_file):
    if uploaded_file:
        # Save PDF using a unique temporary file
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name
            logging.info(f"Saved uploaded PDF to {file_path}")
            email_body = generate_email_from_rag(file_path, email_subject, recipient_name, llm)
        finally:
            # Clean up the temporary file
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        # Search web if no file is provided
        search_results = search(email_subject)
        email_body = generate_email_from_search(recipient_name, email_subject, search_results, llm)
    
    send_email(sender_email, sender_password, recipient_email, email_subject, email_body)
