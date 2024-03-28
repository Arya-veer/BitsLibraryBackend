from library_backend.keyconfig import OPENAI_API_KEY
import os,sys

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


from openai import OpenAI

from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts.chat import ChatPromptTemplate
from library_backend.settings import BASE_DIR

DOCUMENT_DIRECTORY = os.path.join(BASE_DIR,'chatbot','Documents/')

class ChatBot:

    obj = None

    def __init__(self) -> None:

        self.llm = ChatOpenAI()
        self.loader = DirectoryLoader(DOCUMENT_DIRECTORY, glob="**/*.txt", loader_cls=TextLoader)
        self.docs = self.loader.load()
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter()
        self.documents = self.text_splitter.split_documents(self.docs)
        self.vector = FAISS.from_documents(self.documents, self.embeddings)
        self.create_prompt()
        # print(self.PROMPT)
        self.create_response_chain()
        # print(self.retrieval_chain)
    
    @classmethod
    def get_object(cls):
        if not cls.obj:
            cls.obj = ChatBot()
        return cls.obj
        
    def __str__(self) -> str:
        return "Chatbot object"

    def create_prompt(self):
        self.PROMPT = ChatPromptTemplate.from_template("""
                                            Answer the following question based only on the provided context.
                                            <context>
                                            {context}
                                            </context>
                                            Question: {input}
                                            
                                          """)
    
    def create_response_chain(self):  
        document_chain = create_stuff_documents_chain(self.llm, self.PROMPT)
        retriever = self.vector.as_retriever()
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)
        # self.retrieval_chain
    
    def respond(self,question):
        response = self.retrieval_chain.invoke({"input": question})
        return response["answer"]

if __name__ == "__main__":
    # M1
    # chatbot = ChatBot()
    # M2
    chatbot = ChatBot.get_object()
    print(chatbot)
    while True:
        question = input("Ask a question(Or press 0 for exit):")
        if question == "0":
            break
        answer = chatbot.respond(question)
        print(answer)