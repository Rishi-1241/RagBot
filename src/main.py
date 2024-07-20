import os
from dotenv import load_dotenv
from google.cloud import firestore
from google.oauth2 import service_account
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_google_firestore import FirestoreVectorStore
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Tuple, List, Optional
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

import firebase_admin
from firebase_admin import credentials, firestore


class LawSikhoAssistant:
    def __init__(self):
        self._load_env()
        self._initialize_firestore()
        self._initialize_embeddings()
        self._initialize_vectorstore()
        self._initialize_text_splitter()
        self._initialize_retriever()
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)
        self._CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(self._condense_template())
        self.chain = self._create_chain()
        self.chat_history: Optional[List[Tuple[str, str]]] = None

    def _load_env(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def _initialize_firestore(self):
        path = "C:/Users/Prakhar Agrawal/Desktop/Generative AI/Lawsikho/package.json"
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)

    def _initialize_embeddings(self):
        self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)

    def _initialize_vectorstore(self):
        self.vectorstore = FirestoreVectorStore(
            collection='rag_lawsikho2',
            embedding_service=self.embeddings,
        )

    def _initialize_text_splitter(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def _initialize_retriever(self):
        try:
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            print("Retriever initialized successfully.")
        except Exception as e:
            print(f'Error initializing retriever: {e}')

    @staticmethod
    def _prompt_template():
        return """
            You are the sales executive for LawSikho, a firm providing high-quality legal courses. Your role is to deliver friendly and knowledgeable customer service by answering inquiries about our courses and actively promoting enrollment in our programs. Using the context provided, answer the customer's question accurately and precisely.
Instructions:
Highlight the benefits and advantages of our courses based on the user’s needs.
Engage the user by asking questions about their priorities, goals, and background related to legal education.
Use bullet points for clarity in longer responses.
Enhance your response with 1-3 relevant emojis to convey a friendly tone, but avoid overuse.
Important:
Craft responses uniquely, avoiding rhetoric or repetitive promotional statements.
Do not include closing statements that repetitively ask for booking or enrolling.
Contact details: For more information or immediate assistance, call +91 98186 78383.
Example Query Handling:
Context: {context}
Question: {question}

        """

    @staticmethod
    def _condense_template():
        return """
        Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,
        in its original language.
        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:
        """

    @staticmethod
    def _format_chat_history(chat_history: List[Tuple[str, str]]) -> List:
        buffer = []
        for human, ai in chat_history:
            buffer.append(HumanMessage(content=human))
            buffer.append(AIMessage(content=ai))
        return buffer

    def _search_query(self):

        return RunnableBranch(
            (
                RunnableLambda(lambda x: bool(x.get("chat_history"))).with_config(
                    run_name="HasChatHistoryCheck"
                ),
                RunnablePassthrough.assign(
                    chat_history=lambda x: self._format_chat_history(x["chat_history"])
                )
                | self._CONDENSE_QUESTION_PROMPT
                | ChatOpenAI(temperature=0)
                | StrOutputParser(),
            ),
            RunnableLambda(lambda x: x["question"])
        )

    def _create_chain(self):
        return (
            RunnableParallel(
                {
                    "context": self._search_query() | self.retriever,
                    "question": self._search_query() | RunnablePassthrough(),
                }
            )
            | RunnableLambda(lambda x: {
                "context": [chunk for doc in x["context"] for chunk in self.text_splitter.split_text(doc.page_content)],
                "question": x["question"]
            })
            | RunnableLambda(lambda x: {
                "context": [chunk for chunk in x["context"] if len(chunk) < 4096],
                "question": x["question"]
            })
            | ChatPromptTemplate.from_template(self._prompt_template())
            | self.llm
            | StrOutputParser()
        )

    def query(self, user_query: str) -> str:
        input_data = {"question": user_query}
        if self.chat_history:
            input_data["chat_history"] = self.chat_history
        try:
            result = self.chain.invoke(input_data)
        except Exception as e:
            result = f"Error: {e}"
        #print(f"Response: {result}")

        if self.chat_history is None:
            self.chat_history = []
        self.chat_history.append((user_query, result))

        return result

if __name__ == "__main__":
    assistant = LawSikhoAssistant()
    while True:
        query = input("Enter your query: ")
        response = assistant.query(query)
        print(f"Assistant's Response: {response}")