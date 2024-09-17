from langchain_huggingface import HuggingFaceEmbeddings
import os
from faiss_service import create_vector_db
from langchain_community.document_loaders import PyPDFLoader

ENCODING_MODEL_NAME = "intfloat/multilingual-e5-small"

file_path = "./data/docs"

max_pages_to_read = 200
min_char_per_page = 50
max_documents_to_index = 1000

def custom_text_splitter(text, chunk_size=500, overlap=25):
    """Splits text into chunks with a given overlap."""
    text = text.replace('\n', ' ')
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]

def text_from_pdf(pdf_path: str):
    """Extracts and filters text from a PDF, returning the text for relevant pages."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    print(f"Number of pages: {len(pages)}")

    valid_text = [
        page.page_content
        for page in pages[15:max_pages_to_read]
        if len(page.page_content) > min_char_per_page
    ]

    return ' '.join(valid_text)

file_documents = []
pdf_files = [f for f in os.listdir(file_path) if f.lower().endswith(".pdf")]

for file_name in pdf_files:
    full_file_path = os.path.join(file_path, file_name)
    print(f"Processing file: {file_name}")

    try:
        file_content = text_from_pdf(full_file_path)
        if file_content:
            docs = custom_text_splitter(file_content)
            file_documents.extend(docs)
            print(f"Number of documents added: {len(docs)}")

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error with file '{file_name}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred with file '{file_name}': {e}")

file_documents_to_index = file_documents[:max_documents_to_index]
print(f"Total number of documents to index: {len(file_documents_to_index)}")

create_vector_db(file_documents_to_index)
