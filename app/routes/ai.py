from fastapi import APIRouter, HTTPException, status
from models import TranslatorParams
from llm.language_translator import language_translator
import logging
import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/translate")
async def translate(language: str, text: str):
    try:
        params = TranslatorParams(language=language, text=text)
        return language_translator(params=params)
    except Exception as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))