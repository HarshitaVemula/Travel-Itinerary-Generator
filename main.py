import streamlit as st
import os
from streamlit_folium import st_folium
import folium
import json
from langchain_openai import ChatOpenAI

st.set_page_config(layout="wide")


def is_api_key_valid(api_key):
    try:
        response = ChatOpenAI(temperature=0).predict("This is a test prompt.")
    except Exception as e:
        if len(api_key) > 0:
            st.write("Invalid API key")
        return False
    else:
        return True


# st.title("Travel Itinerary Generator")
st.markdown(
    "<h1 style='text-align: center; color: black;'>Travel Itinerary Generator</h1>",
    unsafe_allow_html=True,
)

# Get your openai api key
openai_url = "https://openai.com/blog/openai-api"
st.caption("[Get your OpenAI API key.](%s)" % openai_url)
api_key = st.text_input("Input your API key", type="password")
os.environ["OPENAI_API_KEY"] = api_key
api_key_valid = is_api_key_valid(api_key)

col1, col2 = st.columns(2)

if api_key_valid:
    from prompts import itin_chain, coord_chain
    from templates import itinerary_config, coordinates_config, validation_config

    # Initialize
    with col1:
        st.subheader("Where do you want to travel next?")
        user_input = st.text_input("")

    output = itin_chain({"query": user_input})

    # col1
    if user_input:
        with col1:
            st.write(f"Great! Let's plan your trip!.")
            output[itinerary_config.chain_output_key].replace("$", "\$")
            st.write(output[itinerary_config.chain_output_key])
        is_valid = json.loads(output[validation_config.chain_output_key])[
            validation_config.system_prompt_output_key
        ]

        if is_valid == str(1):
            coord = coord_chain(
                {
                    itinerary_config.chain_output_key: output[
                        itinerary_config.chain_output_key
                    ]
                }
            )
            coord = json.loads(coord[coordinates_config.system_prompt_output_key])
            coord = coord[coordinates_config.chain_output_key]

            locations = list(coord.keys())

            m = folium.Map(location=coord[locations[0]], zoom_start=12)
            for k in locations[1:20]:
                folium.Marker(coord[k], popup=k, tooltip=k).add_to(m)

            with col2:
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                map_data = st_folium(m, width=725, returned_objects=[])
