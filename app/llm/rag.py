from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from redis_handler import redis_handler
from chroma_handler import chroma_handler
from .model import model
from langchain_core.messages import HumanMessage

def rag_model(user_id, user_input):
    system_message = "You are a helpful AI bot knowing upcoming cricket tournament. Also, you can answer general questions about cricket. If user asks about the upcoming cricket tournament, always use retrieved data. If you don't have enough data, tell that you don't know about it. Give the answers directly and politely."
    user_message = HumanMessage(content=user_input)
    
    template = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder("history"),
            ("system", "Here are retrieved information: {retrieved_info}"),
            ("human", "Answer to this question: {question}")
        ]
    )
    
    history_handler = redis_handler()
    history = history_handler.get_messages(user_id, 5)
    
    prompt = template.invoke({
        "history": history,
        "retrieved_info": chroma_handler.query_similar_docs(user_input),
        "question": user_input
     })
            
    response = model.invoke(prompt)
    history_handler.set_messages(user_id, [user_message, response])
    
    return response.content
