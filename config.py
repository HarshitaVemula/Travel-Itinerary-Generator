from dataclasses import dataclass
from pydantic import BaseModel
from typing import Callable, Optional
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from typing import Callable, List, Dict, Optional, Any


@dataclass
class PromptConfig:
  pydantic_object: Optional[BaseModel]
  system_prompt_output_key: Optional[str]
  system_prompt_input_keys: Optional[List[str]]
  human_prompt_input_keys: Optional[List[str]]
  chain_output_key: Optional[str]
  system_template: str = None
  human_template: str = None
  output_parser: Optional[Callable] = PydanticOutputParser
  system_prompt_template: Callable = SystemMessagePromptTemplate
  human_prompt_template: Callable = HumanMessagePromptTemplate