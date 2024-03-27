from openai import OpenAI
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts.chat import ChatPromptTemplate

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
        self.create_response_chain()
    
    @classmethod
    def get_object(cls):
        if not cls.__object:
            try:
                cls.__object = ChatBot()
            except:
                cls.__object = None
        return cls.__object
        


    def create_prompt(self):
        self.PROMPT = ChatPromptTemplate.from_template("""
                                            Answer the following question based only on the provided context. If the question falls out of the CONTEXT, reply with "Sorry, I can't help you with this. Please reach out to the Library Office".
                                            <context>
                                            {context}
                                            </context>
                                            
                                          """)
    
    def create_response_chain(self):  
        document_chain = create_stuff_documents_chain(self.llm, self.PROMPT)
        retriever = self.vector.as_retriever()
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)
        self.retrieval_chain.train(self.docs)
        self.retrieval_chain.save("retrieval_chain")
        
    
    def respond(self,question):
        response = self.retrieval_chain.respond(question)
        return response["answer"]

if __name__ == "__main__":
    chatbot = ChatBot.get_object()
    while True:
        question = input("Ask a question(Or press 0 for exit):")
        if question == "0":
            break
        answer = chatbot.respond(question)
        print(answer)