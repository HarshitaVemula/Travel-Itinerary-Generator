import streamlit as st
import pandas as pd
import numpy as np
from prompts import chain
from templates import itinerary_config, validation_config

#output = chain({'query': "I want to travel to hyderabad for 2 days"})

#from prompts import joke


def parse(output):
    """Parses the itinerary string into a list of bullet points."""
    days = output.strip().split("\n\n")  # Split by newlines
    for day in days:
        for line in day.split('\n'):
          if 'Day' in line:
              st.header(line.strip().strip('-'))
          else:
              st.markdown(line)
         


#Title and prompt
st.title("Travel Itinerary Generator")
user_input = st.text_input("Where do you want to travel next?")
output = chain({'query': user_input})

if user_input:
  st.write(f"Great! Let's plan your trip!.")
  parse(output[itinerary_config.chain_output_key])


