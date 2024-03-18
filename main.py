import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from prompts import itin_chain, locations_chain, coord_chain
from templates import itinerary_config, locations_config, coordinates_config
import json

st.set_page_config(layout="wide")
st.title("Travel Itinerary Generator")


col1, col2 = st.columns(2)

# Initialize
user_input = col1.text_input("Where do you want to travel next?")

output = itin_chain({"query": user_input})

with col1:
    print()


# col1
if user_input:
    with col1:
        st.write(f"Great! Let's plan your trip!.")
        output[itinerary_config.chain_output_key].replace("$", "\$")
        st.write(output[itinerary_config.chain_output_key])

        coord = coord_chain(
            {
                itinerary_config.chain_output_key: output[
                    itinerary_config.chain_output_key
                ]
            }
        )
        coord = json.loads(coord["locations_coord"])
        coord = coord["locations_coord"]

        locations = list(coord.keys())

        m = folium.Map(location=coord[locations[0]], zoom_start=12)
        for k in locations[1:20]:
            folium.Marker(coord[k], popup=k, tooltip=k).add_to(m)

        with col2:
            map_data = st_folium(m, width=725, returned_objects=[])
