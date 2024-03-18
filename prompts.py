import os
from utils import load_secrets
from langchain_openai import ChatOpenAI
from templates import (
    validation_config,
    itinerary_config,
    locations_config,
    coordinates_config,
)
from utils import Template, chain
from langchain.chains.sequential import SequentialChain


# Authorization

os.environ["OPENAI_API_KEY"] = load_secrets()[
    "open_ai_api_key"
]  # Replace with your actual key


# Model

model = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0.5, max_tokens=1000)


# Chains
# Validation
validation_system_prompt = Template(
    template=validation_config.system_template,
    prompt_template=validation_config.system_prompt_template,
    output_parser=validation_config.output_parser,
).get_prompt(
    pydantic_object=validation_config.pydantic_object,
    output_key=validation_config.system_prompt_output_key,
)

validation_human_prompt = Template(
    template=validation_config.human_template,
    prompt_template=validation_config.human_prompt_template,
).get_prompt()

validation_chain = chain(
    llm_model=model,
    list_of_prompt_templates=[validation_system_prompt, validation_human_prompt],
    output_key=validation_config.chain_output_key,
)


# Itinerary generation
itinerary_system_prompt = Template(
    template=itinerary_config.system_template,
    prompt_template=itinerary_config.system_prompt_template,
).get_prompt()

itinerary_human_prompt = Template(
    template=itinerary_config.human_template,
    prompt_template=itinerary_config.human_prompt_template,
).get_prompt()

itinerary_chain = chain(
    llm_model=model,
    list_of_prompt_templates=[itinerary_system_prompt, itinerary_human_prompt],
    output_key=itinerary_config.chain_output_key,
)


# location generation
places_system_prompt = Template(
    template=locations_config.system_template,
    prompt_template=locations_config.system_prompt_template,
    output_parser=locations_config.output_parser,
).get_prompt(
    pydantic_object=locations_config.pydantic_object,
    output_key=locations_config.system_prompt_output_key,
)

places_human_prompt = Template(
    template=locations_config.human_template,
    prompt_template=locations_config.human_prompt_template,
).get_prompt()

locations_chain = chain(
    llm_model=model,
    list_of_prompt_templates=[places_system_prompt, places_human_prompt],
    output_key=locations_config.chain_output_key,
)

# Coordinate generation
coordinates_system_prompt = Template(
    template=coordinates_config.system_template,
    prompt_template=coordinates_config.system_prompt_template,
    output_parser=coordinates_config.output_parser,
).get_prompt(
    pydantic_object=coordinates_config.pydantic_object,
    output_key=coordinates_config.system_prompt_output_key,
)

coordinates_human_prompt = Template(
    template=coordinates_config.human_template,
    prompt_template=coordinates_config.human_prompt_template,
).get_prompt()

coordinates_chain = chain(
    llm_model=model,
    list_of_prompt_templates=[coordinates_system_prompt, coordinates_human_prompt],
    output_key=coordinates_config.chain_output_key,
)


# Final chains
def SeqChain(chains, input_variables):
    chain = SequentialChain(
        chains=chains, input_variables=input_variables, return_all=True, verbose=False
    )
    return chain


itin_chain = SeqChain(
    chains=[validation_chain, itinerary_chain],
    input_variables=validation_config.human_prompt_input_keys,
)


coord_chain = SeqChain(
    chains=[locations_chain, coordinates_chain],
    input_variables=[itinerary_config.chain_output_key],
)
