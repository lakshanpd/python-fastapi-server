from .model import model
from redis_handler import redis_handler
from langchain_core.messages import HumanMessage, SystemMessage

def chat_model(user_id, user_input):
    system_message = SystemMessage(content="You are a helpful AI bot knowing everything in cricket. Answer every question related to cricket in a short way.")
    
    history_handler = redis_handler()
    history = history_handler.get_messages(user_id, 5) 
    
    user_message = HumanMessage(content=user_input)
    
    messages = [system_message] + history + [user_message]    
    response = model.invoke(messages)
    history_handler.set_messages(user_id, [user_message, response])

    return response.content