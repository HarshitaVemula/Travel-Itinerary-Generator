from config import PromptConfig
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Callable, List, Dict, Optional, Any
# Validation

validation_system_template = """
You act as a travel agent that helps user plan their vacation.
      When user makes a request, you need to first check if their ask in a feasible one.
      Here are a few things you can look for the in the request but all these need not be in the request
      1) does it have a location or an origin and a destination
      2) does it have the number of days they want to on the trip for.
{valid}  
      """
validation_human_template = """{query}"""

class ValidationOutputs(BaseModel):
    valid: str = Field(
        description="If the request is feasible then set valid = 1 else set valid = 0 and give a reasoning as to why is it not feasible."
    )


@dataclass
class validation_config(PromptConfig):
  pydantic_object = ValidationOutputs
  human_prompt_input_keys = ['query']
  system_prompt_output_key = 'valid'
  chain_output_key = 'is_valid'
  system_template = validation_system_template
  human_template = validation_human_template


# Itinerary generation
itinerary_system_template ="""You are a travel agent who helps users make exciting travel plans.

    The user's request will be denoted by four hashtags. 
    Now if the user request is {is_valid} valid then generate the itinerary.
    
    Convert the
    user's request into a detailed itinerary describing the places
    they should visit and the things they should do.

    Try to include the specific address of each location.

    Remember to take the user's preferences and timeframe into account,
    and give them an itinerary that would be fun and doable given their constraints.

    Return the itinerary as a bulleted list with clear start and end locations, suggested time at which they should start, how to go to the destination and by
    when will they reach the end location.
    Be sure to mention the type of transit for the trip.
    If specific start and end locations are not given, choose ones that you think are suitable and give specific addresses.
    Your output must be the list and nothing else.
    give the estimated cost of travel, and cost for food and or fun activities they might have to pay for each day.

    here is an example
    Day 1:
      - Start at San Francisco International Airport (SFO) at 9:00 AM. Take a taxi or ride-sharing service to your hotel.
        Check-in at your hotel in downtown San Francisco.
        - Address: 123 Main Street, San Francisco, CA 94101
      - Visit Golden Gate Park
        - Address: 501 Stanyan St, San Francisco, CA 94117
      - Enjoy a leisurely stroll through the park and visit the Japanese Tea Garden. Have lunch at a local restaurant.
      Explore Fishermans Wharf and Pier 39
        - Address: Pier 39, Beach St & The Embarcadero, San Francisco, CA 94133
      - Enjoy the views of the bay, visit the sea lions, and try some local seafood. Take a cable car ride to Lombard Street.
        - Address: Lombard St, San Francisco, CA 94133
      - Experience the famous "crookedest street in the world". Dinner at a restaurant in Chinatown.
        - Address: Chinatown, San Francisco, CA 94133
      - Return to your hotel. Estimated time of return: 9:00 PM.
"""

itinerary_human_template = """####{query}"""


@dataclass
class itinerary_config(PromptConfig):
  chain_output_key = 'agent_suggested_itinerary'
  system_template = itinerary_system_template
  human_template = itinerary_human_template


# Location generator
location_system_template = """  You an agent who converts detailed travel plans into a simple list of locations.

      The itinerary will be denoted by four hashtags. Convert it into
      list of places that they should visit. Try to include the specific address of each location.
      
      Your output should always contain the start and end point of the trip, and may also include a list
      of waypoints. It should also include a mode of transit. The number of waypoints cannot exceed 20.
      If you can't infer the mode of transit, make a best guess given the trip location.

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

      Output:
      itinerary: '
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
        - End the trip at the Tower Bridge (Tower Bridge Rd, London SE1 2UP)'
      Start: Buckingham Palace, The Mall, London SW1A 1AA
      End: Tower Bridge, Tower Bridge Rd, London SE1 2UP
      Waypoints: ["Tower of London, Tower Hill, London EC3N 4AB", "British Museum, Great Russell St, Bloomsbury, London WC1B 3DG", "Oxford St, London W1C 1JN", "Covent Garden, London WC2E 8RF","Westminster, London SW1A 0AA", "St. James's Park, London", "Natural History Museum, Cromwell Rd, Kensington, London SW7 5BD"]
      Transit: driving

      Transit can be only one of the following options: "driving", "train", "bus" or "flight".

      {locations}"""

location_human_template = """####{agent_suggested_itinerary}"""

class locations(BaseModel):
  itinerary: str = Field(descriton = "the travel intinerary that was inputed")
  start: str = Field(description="start location of trip")
  end: str = Field(description="end location of trip")
  waypoints: List[str] = Field(description="list of waypoints")
  transit: str = Field(description="mode of transportation")

@dataclass
class locations_config(PromptConfig):
  pydantic_object = locations
  system_prompt_output_key = 'locations'
  chain_output_key = 'list of locations'
  system_template = location_system_template
  human_template = location_human_template
