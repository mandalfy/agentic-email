import logging
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from tools.file_reader import read_file
from langchain import HuggingFaceHub

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the language model
llm = HuggingFaceHub(
    repo_id="google/flan-t5-base", 
    huggingfacehub_api_token=st.secrets["HUGGINGFACE_TOKEN"]
)

def generate_email_from_rag(pdf_path, query, recipient_name, llm):
    try:
        # Read the content from the PDF
        document_text = read_file(pdf_path)
        if not document_text:
            logging.error("Failed to extract text from PDF.")
            return f"Dear {recipient_name},\n\nSorry, I couldn't extract any useful information from the document.\n\nBest regards,\nAI Agent"

        # Log extracted content
        logging.info(f"Extracted text from PDF ({len(document_text)} characters).")

        # Use a text splitter to ensure the input isn't too long
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(document_text)

        # Use only the first chunk to keep it concise
        context = chunks[0] if chunks else "No relevant content found."

        # Construct the prompt
        prompt = f"Summarize the following information about {query}:\n\n{context}"

        # Generate summary using LLM
        summary = llm.invoke(prompt)

        # Construct the email
        email_body = f"Dear {recipient_name},\n\n{summary}\n\nBest regards,\nAI Agent"

        return email_body

    except Exception as e:
        logging.error(f"Error in generate_email_from_rag: {e}")
        return f"Dear {recipient_name},\n\nAn error occurred while processing your request.\n\nBest regards,\nAI Agent"
