from .model import model
from database.redis_handler import redis_handler
from langchain_core.messages import HumanMessage, SystemMessage

def chat_model(user_id, user_input):
    system_message = SystemMessage(content="You are a helpful AI bot knowing everything in cricket. Answer every question related to cricket in a short way.")
    history = redis_handler.get_messages(user_id, 5) 
    user_message = HumanMessage(content=user_input)
    
    messages = [system_message] + history + [user_message]    
    response = model.invoke(messages)
    
    redis_handler.set_messages(user_id, [user_message, response])

    return response.content

def clear_chat_history(user_id):
    redis_handler.delete_all(user_id)
    