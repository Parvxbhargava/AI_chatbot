from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings  # 🔁 Changed from OpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI  # ✅ still works with OpenRouter
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Set OpenRouter API key
os.environ["OPENROUTER_API_KEY"] = os.getenv("API_KEY")

# ✅ Load text and split into chunks
loader = TextLoader("app/data.txt")
docs = loader.load()
print(f"✅ Loaded {len(docs)} documents")
print("📄 First 300 chars of loaded document:")
print(docs[0].page_content[:300])

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)
print(f"✅ Split into {len(chunks)} chunks")
print("🔹 First chunk preview:")
print(chunks[0].page_content[:300])


# ✅ Use free HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ✅ Create FAISS vectorstore
print("creating faiss")
vectorstore = FAISS.from_documents(chunks, embeddings)
print("✅ Vectorstore created with", len(chunks), "documents")

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ✅ Use OpenRouter model via ChatOpenAI
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",  # 👈 OpenRouter URL
    api_key=os.getenv("API_KEY"),  # 👈 Key from .env
    model="openai/gpt-3.5-turbo",     # 👈 Pick any OpenRouter-supported model
    temperature=0
)

# ✅ RAG chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# ✅ Callable function
def get_rag_answer(query):
    return qa_chain.run(query)







