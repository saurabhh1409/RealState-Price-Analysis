import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast

from pages.pricepredictor import property_type

st.set_page_config(page_title="Ploting Demo")
st.title("Analysis")

new_df = pd.read_csv("datasets/data_viz1.csv")
df = pd.read_csv("datasets/gurgaon_properties_missing_value_imputation.csv")
df1 = pd.read_csv("datasets/gurgaon_properties.csv")
#st.dataframe(new_df)


group_df = new_df[['sector', 'price','price_per_sqft','built_up_area','latitude','longitude']].groupby('sector').mean()

st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)

st.header('WordCloud For Each Sector')

# Merge dataframes
wordcloud_df = df1.merge(df, left_index=True, right_index=True)[['features', 'sector']]

#Clean and parse 'features'
wordcloud_df = wordcloud_df.dropna(subset=['features'])
wordcloud_df['features'] = wordcloud_df['features'].apply(ast.literal_eval)

#Sector selector
sectors = sorted(wordcloud_df['sector'].dropna().unique())
selected_sector = st.selectbox("Select a Sector", sectors)

# Filter data for selected sector
sector_df = wordcloud_df[wordcloud_df['sector'] == selected_sector]

#Flatten feature list
features_list = []
for item in sector_df['features']:
    features_list.extend(item)

#Generate WordCloud
if features_list:
    feature_text = " ".join(features_list)

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=set(['s']),
        min_font_size=10
    ).generate(feature_text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
else:
    st.warning("No features available for the selected sector.")

st.header("Area vs Price")
property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header("BHK Pie Chart")
sector_options =new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox("select sector", sector_options)
if selected_sector == 'overall':
    fig2 = px.pie(new_df , names= 'bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)