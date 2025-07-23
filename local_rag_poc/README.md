# Local RAG POC

This is a chatbot with a simple RAG implementation.  The goal was to do so while running everything locally.

## Setup

In addition to setting this up like any other python venv project, you will also need Ollama running, and have pulled the following models:

- llama3.2
- mxbai-embed-large

`vector.py` will create `middangeard_db` if it doesn't exist.  If it does, it will not load data from `middangeard_data.csv`.  Delete the `*_db` dir to cause it to reload the csv on the next run.
