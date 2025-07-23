from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever


model = OllamaLLM(model="llama3.2")

template = """
You are an expert in Middangeard, a fantasy world. You have access to a vast amount of knowledge about its history, culture, and inhabitants.
You will be provided with some relevant info and a question. Use the context to answer the question accurately

Here is some relevant info: {context}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

hr = "-=" * 20
while True:
    print(hr)
    print("Ask a question about Middangeard:")
    user_question = input()
    if user_question.lower() == "exit":
        break

    context = retriever.invoke(user_question)
    result = chain.invoke({"context": context, "question": user_question})

    print("Answer:", result)
