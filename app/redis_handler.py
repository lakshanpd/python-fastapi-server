import redis
from dotenv import load_dotenv
import os
import json
from langchain.schema import HumanMessage, AIMessage, BaseMessage

load_dotenv()

class redis_handler:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv("redis_host"),
            port=os.getenv("redis_port"),
            db=int(os.getenv("redis_db_number", 0)),
            decode_responses=True
        )

    def set_messages(self, user_id, messages: list[BaseMessage]):
        for message in messages:
            serialized = json.dumps({
                "type": message.__class__.__name__,
                "data": {
                    "content": message.content
                }
            })
            self.client.rpush(user_id, serialized)

    def get_messages(self, user_id, N):
        messages_raw = self.client.lrange(user_id, -6, -1)
        messages = []
        for m in messages_raw:
            parsed = json.loads(m)
            if parsed["type"] == "HumanMessage":
                messages.append(HumanMessage(content=parsed["data"]["content"]))
            elif parsed["type"] == "AIMessage":
                messages.append(AIMessage(content=parsed["data"]["content"]))
        return messages

    def delete_all(self, user_id):
        self.client.delete(user_id)
