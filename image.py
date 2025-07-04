import requests
from bs4 import BeautifulSoup
import urllib.parse
location_df = pickle.load(open('datasets/location_distance_new.pkl','rb'))

def fetch_google_image_url(query):
    query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query}&tbm=isch"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all("img")

    # Skip first image (Google's logo or irrelevant)
    for img in images[1:]:
        src = img.get("src")
        if src and src.startswith("http"):
            return src
    return None


import streamlit as st


@st.cache_data
def get_image_url_cached(property_name):
    return fetch_google_image_url(property_name)


st.title("Apartments with Images")

# Assuming you already have your DataFrame loaded
for apt in location_df["PropertyName"]:
    st.subheader(apt)
    image_url = get_image_url_cached(apt)

    if image_url:
        st.image(image_url, use_column_width=True)
    else:
        st.write("Image not found.")
