from langchain.document_loaders import PyPDFLoader

def read_file(file_path):
    """Read text from a PDF file using PyPDFLoader."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return " ".join([doc.page_content for doc in documents])