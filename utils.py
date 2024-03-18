from dotenv import load_dotenv
from pathlib import Path
from typing import Callable, List, Dict, Optional, Any
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain
import os


def load_secrets():
    load_dotenv()
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    google_genai_api_key = os.getenv("GOOGLE_PALM_API_KEY")
    open_ai_api_key = os.getenv("OPEN_AI_API_KEY")

    return {
        "google_genai_api_key": google_genai_api_key,
        "open_ai_api_key": open_ai_api_key,
    }


class Template:
    def __init__(
        self,
        template: str = "",
        prompt_template: Callable = None,
        output_parser: Callable = None,
    ):
        self.template = template
        self.prompt_template = prompt_template
        self.output_parser = output_parser

    def get_prompt(
        self,
        input_variables: List[Any] = [],
        pydantic_object: Optional[BaseModel] = None,
        output_key: Optional[str] = None,
    ):
        partial_variables = {}
        if output_key and self.output_parser and pydantic_object:
            parser = self.output_parser(pydantic_object=pydantic_object)
            partial_variables = {output_key: parser.get_format_instructions()}
        prompt = PromptTemplate(
            template=self.template,
            input_variables=input_variables,
            partial_variables=partial_variables,
        )
        if self.prompt_template:
            prompt_template = self.prompt_template(prompt=prompt)
            return prompt_template
        else:
            return None


def chain(
    llm_model: Callable = None,
    list_of_prompt_templates: List = [],
    verbose=True,
    output_key: str = None,
):
    chat_prompt = ChatPromptTemplate.from_messages(list_of_prompt_templates)
    chain = LLMChain(
        llm=llm_model, prompt=chat_prompt, verbose=verbose, output_key=output_key
    )
    return chain
