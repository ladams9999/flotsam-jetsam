from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

working_dir = os.path.dirname(os.path.abspath(__file__))
db_location = os.path.join(working_dir, "middangeard_db")
filename = os.path.join(working_dir, "middangeard_data.csv")
add_documents = False if os.path.exists(db_location) else True

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db = Chroma(
    collection_name="middangeard",
    persist_directory=db_location,
    embedding_function=embeddings,
)

if add_documents:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} does not exist. Please provide the data file.")
    df = pd.read_csv(filename)

    documents = []
    ids = []
    for an_index, a_row in df.iterrows():
        id = str(an_index)
        page_content = f"{a_row['title']} {a_row['data']}"
        metadata = {
            "scope": a_row["scope"],
        }
        document = Document(page_content=page_content, metadata=metadata, id=id)
        documents.append(document)
        ids.append(id)

    db.add_documents(documents=documents, ids=ids)

retriever = db.as_retriever(search_kwargs={"k": 3})
