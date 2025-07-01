# 🚀 Python FastAPI Server

This repository demonstrates how to build a modern backend server using **FastAPI**, a high-performance Python web framework for building APIs with asynchronous support (ASGI). The project is intended as a learning resource for backend development with FastAPI and includes integrations with databases, JWT-based authentication, AI functionalities, and **Retrieval-Augmented Generation (RAG)** using ChromaDB.

---

## ✨ Key Features

- ✅ Build modular, well-structured APIs using FastAPI
- 🛢️ Connect with MySQL and Redis databases
- 🧠 Integrate a RAG pipeline with ChromaDB for intelligent document Q&A
- 🤖 Include AI models for language translation & chatbot
- 🔐 Implement authentication using JWT tokens
- ⚙️ Use environment variables and type validation via `.env` and Pydantic

---

## 📦 Modules

### 📘 1. Develop APIs Using FastAPI

The project uses the context of an **upcoming cricket tournament** to demonstrate various API functionalities. Special focus is given to:

- Clean code structure with modular design
- Exception handling
- Middleware for JWT authentication on protected routes

### 🛠️ 2. Connect with Databases

- **MySQL**: Used as the primary persistent storage
- **Redis**: Used for caching chat history for the chatbot (for fast retrieval)

### 🧠 3. Retrieval-Augmented Generation (RAG)

This project integrates a **RAG pipeline** to enhance LLM responses using relevant external knowledge:

- **Document Embedding**:

  - Text documents are chunked using `SemanticChunker` from `langchain_experimental`
  - Embeddings are generated via `GoogleGenerativeAIEmbeddings`

- **Vector Store**:

  - ChromaDB is used as the vector database
  - Documents are stored, queried, and retrieved based on similarity

- **Similarity-Based Retrieval**:

  - A user query is embedded and compared to stored chunks
  - Top-k similar documents are retrieved and passed to the LLM

- **Use Case**:
  - Accurate answers for queries about tournament registration, logistics, history, etc.

### 🤖 4. Integrate AI into the Application

Includes two AI features:

- Language Translator
- Chat Assistant that maintains conversational memory over a session

Both models are served via protected API endpoints.

### 🧰 5. Other Technologies

- JWT token handling with access & refresh tokens
- `.env` file for managing environment variables securely
- Type validation using **Pydantic**
- Request interceptor middleware for authentication

---

## 🔁 API Flow

Here’s the flow to try out the APIs:

1. **Register a user**

   ```
   POST /register
   ```

2. **Login and retrieve tokens**

   ```
   POST /login
   ```

   Returns: `access_token` and `refresh_token`

3. **Refresh token** (if expired)

   ```
   POST /refresh-token
   ```

4. **Use protected routes** with

   ```
   Authorization: Bearer <access_token>
   ```

   Example protected routes:

   - `/translate` – Language translation
   - `/chat` – Ask a question to the chatbot
   - `/clear-chat` – Clear conversation memory
   - `/ask-assistant` – Ask a question to the rag based chatbot

---

## ⚙️ Setup Instructions

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL**

   Create a MySQL database using the provided schema.

3. **Set up Redis**

   Install and run Redis.

4. **Obtain Gemini API key**

   Required for chatbot and translation features.

5. **Create a `.env` file** in the root directory:
   ```env
   host=<your_mysql_host>
   user=<your_mysql_user>
   password=<your_mysql_password>
   database=<your_database_name>
   secret_key=<your_jwt_secret_key>
   GOOGLE_API_KEY=<your_gemini_api_key>
   redis_host=<your_redis_host>
   redis_port=<your_redis_port>
   redis_db_number=<your_redis_db_number>
   ```
