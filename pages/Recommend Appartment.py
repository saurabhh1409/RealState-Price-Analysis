import pandas as pd
import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Recommend")
st.title('Recommendation')

location_df = pickle.load(open('datasets/location_distance_new.pkl','rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl','rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties
    })

    return recommendations_df

# Session state to keep selected apartment
if 'result_ser' not in st.session_state:
    st.session_state.result_ser = None
if 'selected_apartment' not in st.session_state:
    st.session_state.selected_apartment = None

# Step 1: Select location + radius
st.subheader("1. Choose Location and Radius")
selected_location = st.selectbox("Location", sorted(location_df.columns.to_list()))
radius = st.number_input("Radius (km)", min_value=0.0, value=3.0, step=0.5)

# Button to trigger search
if st.button("Search"):
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

    if result_ser.empty:
        st.warning("No apartments found within selected radius.")
        st.session_state.result_ser = None
    else:
        st.session_state.result_ser = result_ser  # Save to session

# Step 2: Show apartments only if search was done
if st.session_state.result_ser is not None:
    st.subheader("2. Select One Apartment")

    result_ser = st.session_state.result_ser
    formatted_apts = [f"{apt}  -  {round(dist / 1000, 1)} km" for apt, dist in result_ser.items()]
    apt_mapping = dict(zip(formatted_apts, result_ser.index))

    selected_display = st.radio("Nearby Apartments", formatted_apts, key="apt_radio")
    st.session_state.selected_apartment = apt_mapping[selected_display]

    # Step 3: Button to trigger recommendations
    if st.button("Show Recommendations"):
        selected_apartment = st.session_state.selected_apartment
        st.subheader(f"3. Apartments Similar to: {selected_apartment}")
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        st.dataframe(recommendation_df)


#st.title("Recommend Appartments")
#selected_appartment = st.selectbox('Select an Appartments' , sorted(location_df.index.to_list()))

#if st.button("Recommend"):
    #recommendation_df = recommend_properties_with_scores(selected_appartment)
    #st.dataframe(recommendation_df)