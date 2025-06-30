from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import getpass
import asyncio
from langchain_community.document_loaders import DirectoryLoader

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")
  
class ChromaHandler:
    def __init__(self):
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.chunker = SemanticChunker(embedding)
        
    async def make_chunks(self, dir_path):
        loader = DirectoryLoader(dir_path, glob="*.txt")
        docs = loader.load()
        
        return await self.chunker.atransform_documents(docs)

if __name__ == "__main__":
    test_obj = ChromaHandler()
    result = asyncio.run(test_obj.make_chunks("./data/"))
    print(result)