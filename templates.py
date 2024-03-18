from config import PromptConfig
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Callable, List, Dict, Optional, Any

# Validation

validation_system_template = """
You are a travel agent. Figure out is a user's request is {valid}. This could depend on the where 
they want to travel, when they want ot travel, how they want to travel or within what budget they want to travel.
if you think it is not feasible update the user request.
      """
validation_human_template = """{query}"""


class ValidationOutputs(BaseModel):
    valid: str = Field(
        description="If the request is feasible then set valid = 1 else set valid = 0"
    )


@dataclass
class validation_config(PromptConfig):
    pydantic_object = ValidationOutputs
    human_prompt_input_keys = ["query"]
    system_prompt_output_key = "valid"
    chain_output_key = "is_valid"
    system_template = validation_system_template
    human_template = validation_human_template


# Itinerary generation
itinerary_system_template = """You are a travel agent who helps users make exciting travel plans.

    The user's request will be denoted by four hashtags. 
    valid = {is_valid}
    if valid = 1, then generate a travel plan.
    
    Convert the user's request into a detailed itinerary describing the places they should visit and the things they should do. 
    Remember to take the user's preferences and timeframe into account,
    and give them an itinerary that would be fun and doable given their constraints. Also tell them the means of transportation by which they should get from 
    one place to another. 
    Recommed good hotels to stay and places to eat. Include what time they should they should reach different places.

    if the user reuests the trip to be planned with in a certain budget, do so and give them a day wise budget breakdown.


"""

itinerary_human_template = """####{query}"""


@dataclass
class itinerary_config(PromptConfig):
    chain_output_key = "agent_suggested_itinerary"
    system_template = itinerary_system_template
    human_template = itinerary_human_template


# Location generator
location_system_template = """  
      From the itinerary suggested, extract the list of places that were suggested for the user to visit.
      The user's request will be denoted by four hashtags. 
      For example:

      ####
      Itinerary for a 2-day driving trip within London:
      - Day 1:
        - Start at Buckingham Palace (The Mall, London SW1A 1AA)
        - Visit the Tower of London (Tower Hill, London EC3N 4AB)
        - Explore the British Museum (Great Russell St, Bloomsbury, London WC1B 3DG)
        - Enjoy shopping at Oxford Street (Oxford St, London W1C 1JN)
        - End the day at Covent Garden (Covent Garden, London WC2E 8RF)
      - Day 2:
        - Start at Westminster Abbey (20 Deans Yd, Westminster, London SW1P 3PA)
        - Visit the Churchill War Rooms (Clive Steps, King Charles St, London SW1A 2AQ)
        - Explore the Natural History Museum (Cromwell Rd, Kensington, London SW7 5BD)
        - End the trip at the Tower Bridge (Tower Bridge Rd, London SE1 2UP)
      #####

      Based on the travel plan above here is the list of places that were suggested to the user to visit.
      The output should look like this - 

      Output:
      locations = ["Buckingham Palace","Tower of London", "British Museum", "Covent Garden", 
      "Westminster Abbey", "Churchill War Rooms", "Natural History Museum", "Tower Bridge"]
    

{locations}"""

location_human_template = """####{agent_suggested_itinerary}"""


class locations(BaseModel):
    locations: List = Field(descripton="List of places suggested to the user")


@dataclass
class locations_config(PromptConfig):
    pydantic_object = locations
    system_prompt_output_key = "locations"
    chain_output_key = "locations"
    system_template = location_system_template
    human_template = location_human_template


# Coordinates Generator
coordinates_system_template = """  
Given a list of places, get their latitute and longitude
the output should be a dictionary.

The user's request will be denoted by four hashtags. 

for example 
if input is ####["Buckingham Palace","Tower of London"]
output should be 

  "Buckingham Palace": [51.5014, -0.1419],
  "Tower of London": [51.5081, -0.0759]

{locations_coord}
      """

coordinates_human_template = """####{locations}"""


class locations_coord(BaseModel):
    locations_coord: Dict = Field(
        descripton="dictionary of list of coordinates of various place"
    )


@dataclass
class coordinates_config(PromptConfig):
    pydantic_object = locations_coord
    system_prompt_output_key = "locations_coord"
    chain_output_key = "locations_coord"
    system_template = coordinates_system_template
    human_template = coordinates_human_template
