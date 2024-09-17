import logging
import os

from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

ENCODING_MODEL_NAME = "intfloat/multilingual-e5-small"


def get_docs_length(index_path, embeddings):
    test_index = FAISS.load_local(
        index_path, embeddings, allow_dangerous_deserialization=True
    )
    test_dict = test_index.docstore._dict
    return len(test_dict.values())


def create_vector_db(values: list):
    try:
        DB_FAISS_PATH = f"data/documentstore"
        if not os.path.exists(DB_FAISS_PATH):
            print(f"Creating Vector DB at {DB_FAISS_PATH}...")
            texts = []

            for value in values:
                texts.append(Document(page_content=value, metadata={"source": "local"}))

            embeddings = HuggingFaceEmbeddings(
                model_name=ENCODING_MODEL_NAME,
                model_kwargs={"device": "cpu"},
            )

            db = FAISS.from_documents(texts, embeddings)
            db.save_local(DB_FAISS_PATH)

            print(
                f"{get_docs_length(DB_FAISS_PATH,embeddings)} docs created & stored at {DB_FAISS_PATH}"
            )
        else:
            print(f"{DB_FAISS_PATH} DB already exists")
    except Exception as e:
        print(f"Error creating DB: {e}")


def read_from_vector_db(question: str, top_k: int):
    try:
        DB_FAISS_PATH = f"data/documentstore"
        print(f"Loading Vector DB from {DB_FAISS_PATH}...")
        embeddings = HuggingFaceEmbeddings(
            model_name=ENCODING_MODEL_NAME,
            model_kwargs={"device": "cpu"},
        )

        db = FAISS.load_local(
            DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True
        )

        results_with_scores = db.similarity_search_with_score(
            question,
            k=top_k,
        )
        result_list = []
        for doc, score in results_with_scores:
            result_list.append(doc.page_content)
        return result_list
    except Exception:
        return []