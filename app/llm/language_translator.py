from langchain_core.prompts import ChatPromptTemplate
from .model import model
from utils.models import TranslatorParams

def language_translator(params: TranslatorParams):
    system_template = "translate the following from English to {language}. just give the translation most possible one. don't give any extra details."

    prompt_template = ChatPromptTemplate(
        [('system', system_template), ('user', "{text}")]
    )

    prompt = prompt_template.invoke({"language": params.language, "text": params.text})
    response = model.invoke(prompt)
    
    return response.content
