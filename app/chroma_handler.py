from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import getpass
import asyncio
from langchain_community.document_loaders import DirectoryLoader
from langchain_chroma import Chroma
from uuid import uuid4
import chromadb

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
  
class ChromaHandler:
    def __init__(self):
        self.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.chunker = SemanticChunker(self.embedding)
        self.persistent_client = chromadb.PersistentClient()
        
    def get_collection_name(self, dir_path):
        return os.path.splitext(os.path.basename(dir_path))[0]
        
    async def make_chunks(self, dir_path):
        loader = DirectoryLoader(dir_path, glob="*.txt")
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = self.get_collection_name(doc.metadata["source"])

        chunks = await self.chunker.atransform_documents(docs)

        return chunks
    
    async def sync_document_data(self, dir_path):
        chunks = await self.make_chunks(dir_path)
        
        existing_collections = [col.name for col in self.persistent_client.list_collections()]
        if "document" in existing_collections:
            self.persistent_client.delete_collection("document")

        vector_store = Chroma(
            collection_name="document",
            embedding_function=self.embedding,
            client=self.persistent_client,  
        )
                           
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        vector_store.add_documents(documents=chunks, ids=uuids)
        
    def query_similar_docs(self, query):
        vector_store = Chroma(
            collection_name="document",
            embedding_function=self.embedding,
            client=self.persistent_client,  
        )
        return vector_store.similarity_search_with_score(query=query, k=2)
            
chroma_handler = ChromaHandler()
