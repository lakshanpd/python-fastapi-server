from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import getpass
import asyncio
from langchain_community.document_loaders import DirectoryLoader
import chromadb

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
  
class ChromaHandler:
    def __init__(self):
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.chunker = SemanticChunker(embedding)
        self.chroma_client = chromadb.PersistentClient()

        
    async def make_chunks(self, dir_path):
        loader = DirectoryLoader(dir_path, glob="*.txt")
        docs = loader.load()

        chunks_dict = {}
        for doc in docs:
            file_name = doc.metadata["source"]
            chunks_dict[file_name] = []

        chunks = await self.chunker.atransform_documents(docs)

        for chunk in chunks:
            file_name = chunk.metadata["source"]
            chunks_dict[file_name].append(chunk)

        return chunks_dict

    
    # def add_to_store(self, dir_path):
    #     collection_names = [f.split(".")[0] for f in os.listdir(dir_path) if f.endswith(".txt")]
    #     chunks = self.make_chunks(dir_path)
    #     for collection_name in collection_names:
    #         collection = self.chroma_client.get_or_create_collection(collection_name)
            
if __name__ == "__main__":
    test_obj = ChromaHandler()
    result = asyncio.run(test_obj.make_chunks("./data/"))
    print(result)
    # test_obj.make_collections("./data/")