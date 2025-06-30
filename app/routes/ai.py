from fastapi import APIRouter, HTTPException, status, Depends
from models import TranslatorParams, ChatModelParams
from llm.language_translator import language_translator
from llm.chat_model import chat_model, clear_chat_history
from llm.rag import rag_model
import logging
import traceback
from auth import validate_token

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/translate")
async def translate(request = Depends(validate_token)):
    try:
        params = TranslatorParams(language=request["request"].query_params["language"], text=request["request"].query_params["text"])
        return language_translator(params=params)
    except Exception as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/chat")
async def chat(request = Depends(validate_token)):
    try:
        body = await request["request"].json()
        params = ChatModelParams(user_id=request["user"]["id"], user_input=body["user_input"])
        
        return chat_model(params.user_id, params.user_input)
    except Exception as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/clear-chat")
async def clear_chat(request = Depends(validate_token)):
    try:
        clear_chat_history(request["user"]["id"])
        return {
            "status": status.HTTP_200_OK,
            "message": "chat history is cleared successfully."
        }
    except Exception as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/ask-assistant")
async def ask_assistant(request = Depends(validate_token)):
    try:
        body = await request["request"].json()
        params = ChatModelParams(user_id=request["user"]["id"], user_input=body["user_input"])
        
        return rag_model(params.user_id, params.user_input)
    except Exception as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    