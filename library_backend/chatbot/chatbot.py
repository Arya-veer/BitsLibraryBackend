from openai import OpenAI

from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

class ChatBot:

    __object = None

    def __init__(self) -> None:

        self.client = OpenAI()
        self.llm = ChatOpenAI()
        self.loader = DirectoryLoader('./Documents/', glob="**/*.txt", loader_cls=TextLoader)
        self.docs = self.loader.load()
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter()
        self.documents = self.text_splitter.split_documents(self.docs)
        self.vector = FAISS.from_documents(self.documents, self.embeddings)
        self.create_prompt()
        self.create_response_chain
    
    @staticmethod
    def get_object():
        if not __object:
            __object = ChatBot()
        return __object
        


    def create_prompt(self):
        self.PROMPT = self.ChatPromptTemplate.from_template("""
                                            Answer the following question based only on the provided context. If the question falls out of the CONTEXT, reply with "Sorry, I can't help you with this. Please reach out to the Library Office".
                                            <context>
                                            {context}
                                            </context>

                                            Question: {input}
                                          """)
    
    def create_response_chain(self):  
        document_chain = create_stuff_documents_chain(self.llm, self.PROMPT)
        retriever = self.vector.as_retriever()
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    def respond(self,question):
        response = self.retrieval_chain.invoke({"input": question})
        return response["answer"]

if __name__ == "__main__":
    # M1
    # chatbot = ChatBot()
    # M2
    chatbot = ChatBot.get_object()

    while True:
        question = input("Ask a question(Or press 0 for exit):")
        if question == "0":
            break
        answer = chatbot.respond(question)
        print(answer)