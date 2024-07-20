import os
import json
from dotenv import load_dotenv
from google.cloud import firestore
from google.oauth2 import service_account
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_google_firestore import FirestoreVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Tuple, List, Optional
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize Firestore client
path = "C:/Users/Prakhar Agrawal/Desktop/Generative AI/Lawsikho/package.json"

cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Initialize FirestoreVectorStore
vectorstore = FirestoreVectorStore(
    collection='rag_lawsikho3',
    embedding_service=embeddings,
)

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Initialize retriever
try:
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    print("Retriever initialized successfully.")
except Exception as e:
    print(f'Error initializing retriever: {e}')

# Initialize ChatOpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def prompt_template():
    return """
        You are the virtual assistant for LawSikho, a firm providing high-quality legal courses. Your role is to deliver friendly and knowledgeable customer service by answering inquiries about our courses and promoting the LawSikho brand.
        Our courses are tutored by experienced professionals who have achieved significant success in the legal field.
        We provide extensive placement opportunities with top legal firms and organizations.

        Follow these guidelines to ensure efficient service:
        - Understand the Query: create multiple steps to solve the user's query.
        - Context Retrieval: Use the context from the retriever to obtain the necessary context for solving the user's query.

        You are provided with the context and the question and using the context only you have to answer the question.
        Using the context: {context} answer the question: {question}.

        Do not assume anything, just give the answer that you have retrieved from the context only.

        Your goal is to provide precise and helpful responses to all customer inquiries.

        Contact details: For more information or immediate assistance, call +91 98186 78383.
    """

def _format_chat_history(chat_history: List[Tuple[str, str]]) -> List:
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

def _search_query():
    return RunnableBranch(
        # If input includes chat_history, we condense it with the follow-up question
        (
            RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
                run_name="HasChatHistoryCheck"
            ),
            RunnablePassthrough.assign(
                chat_history=lambda x: _format_chat_history(x["chat_history"])
            )
            | CONDENSE_QUESTION_PROMPT
            | ChatOpenAI(temperature=0)
            | StrOutputParser(),
        ),
        # Else, we have no chat history, so just pass through the question
        RunnableLambda(lambda x: x["question"])
    )

def _condense_template():
    return """
    Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,
    in its original language.
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:
    """

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_condense_template())

chain = (
    RunnableParallel(
        {
            "context": _search_query() | retriever,
            "question": _search_query() | RunnablePassthrough(),
        }
    )
    # Split the retrieved documents into chunks
    | RunnableLambda(lambda x: {
        "context": [chunk for doc in x["context"] for chunk in text_splitter.split_text(doc.page_content)],
        "question": x["question"]
    })
    # Filter the chunks to ensure they fit within the token limit
    | RunnableLambda(lambda x: {
        "context": [chunk for chunk in x["context"] if len(chunk) < 4096],
        "question": x["question"]
    })
    | ChatPromptTemplate.from_template(prompt_template())
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    chat_history: Optional[List[Tuple[str, str]]] = None
    while True:
        query = input("Enter your query: ")
        input_data = {"question": query}
        if chat_history:
            input_data["chat_history"] = chat_history
        try:
            result = chain.invoke(input_data)
        except Exception as e:
            result = f"Error: {e}"
        print(f"Response: {result}")
        if chat_history is None:
            chat_history = []
        chat_history.append((query, result))
