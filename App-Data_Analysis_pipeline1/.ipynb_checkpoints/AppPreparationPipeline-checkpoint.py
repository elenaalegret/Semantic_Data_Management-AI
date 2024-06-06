#################################
### App Preparation Pipeline ###
#################################
## Description:
# This file comprises the data preparation pipeline for the BCN Map4Tourism application.
# Inputs:
#  - JDBC connections to DuckDB for loading datasets: Using Spark to directly query DuckDB where t
#     he datasets are initially stored in tables.
#
# Outputs:
#  - Enhanced and formatted tables in DuckDB: After processing, the data is stored back into DuckDB tables.

## Imports: Importing necessary libraries for data processing and visualization
import streamlit as st
from pprint import pprint
import warnings
import matplotlib.pyplot as plt
import pickle
import random
import pandas as pd 
import base64

from torchkge.data_structures import KnowledgeGraph
from rdflib import Graph


# Loading the trusted datasets for explotation
##############################################
## Data Loading using Spark
# Load the RDF graph
g = Graph()
g.parse("./../data/explotation_zone/RDFGraph_Visualitzation.ttl", format="ttl")

# .............................................................................

# Data Processing: Calculating average ratings and enriching location data with these ratings
avg_ratings = df_reviews.groupBy('location_id').agg(avg('rating').alias('avg_rating'))
df_locations = df_locations.join(avg_ratings, on='location_id', how='left')

#################################
###  Dictionaries for Parsing ###
#################################

# Visualization Dictionaries: Predefined colors and icons for mapping different city areas and location types
colors = {
    'Gràcia': 'lightblue', 'Sant Martí': 'green', 'Horta-Guinardó': 'red',
    'Les Corts': 'purple', 'Sants-Montjuïc': 'orange', 'Nou Barris': 'pink',
    'Sarrià-Sant Gervasi': 'cadetblue', 'Eixample': 'beige', 'Sant Andreu': 'lightgray',
    'Ciutat Vella': 'lightgreen'
}
location_icons = {
    'restaurant': 'cutlery', 'attraction': 'star'
}

#################################
###        Functions          ###
#################################
# Apartment Filtration Function: 
#    -> Sidebar controls for dynamic user-driven data filtering
def filter_apartments(data_frame):
    with st.sidebar.expander(" 🧹 Apartments Filtration"):
        # Filter based on user selections for review scores and price
        review_min = st.slider("🌟 Review Score", min_value=0, max_value=10, value=7)
        data_frame = data_frame.filter(data_frame['review_scores_value'] >= review_min)

        price_max = st.slider("Maximum Price per Night", min_value=0, max_value=int(data_frame.select(max("price")).first()[0]), value=80)
        data_frame = data_frame.filter(data_frame['price'] < price_max)

        # Advanced filtering options: room types, bathrooms, beds, and minimum nights
        more_filters_active = st.checkbox("More Filtration")
        if more_filters_active:
            room_types = data_frame.select("room_type").distinct().rdd.flatMap(lambda x: x).collect()
            selected_room_types = st.multiselect("Room Types", room_types, default=room_types)
            data_frame = data_frame.filter(data_frame['room_type'].isin(selected_room_types))

            bathrooms_min = st.slider("Minimum Bathrooms", min_value=0, max_value=int(data_frame.select(max("bathrooms")).first()[0]), value=0)
            data_frame = data_frame.filter(data_frame['bathrooms'] >= bathrooms_min)

            beds_min = st.slider("Minimum Beds", min_value=0, max_value=int(data_frame.select(max("beds")).first()[0]), value=0)
            data_frame = data_frame.filter(data_frame['beds'] >= beds_min)

            min_nights = st.slider("Minimum Nights", min_value=0, max_value=int(data_frame.select(max("minimum_nights")).first()[0]), value=0)
            data_frame = data_frame.filter(data_frame['minimum_nights'] >= min_nights)

    return data_frame

# Crime Analysis Function: Analyzing crime data and visualizing statistics for selected neighborhoods
def criminal_implementation(dataset, selected_neighborhoods):
    selected_neighborhoods_list = [neighborhood for neighborhood, selected in selected_neighborhoods.items() if selected]
    filtered_criminal_data = dataset.filter(dataset['area_basica_policial'].isin(selected_neighborhoods_list))

    crime_counts = filtered_criminal_data.groupBy('area_basica_policial', 'ambit_fet').count()
    total_crimes = crime_counts.groupBy('area_basica_policial').sum('count').withColumnRenamed("sum(count)", "total_count")
    crime_details = crime_counts.join(total_crimes, 'area_basica_policial')
    total_crimes_all_neighborhoods = total_crimes.groupBy().sum('total_count').collect()[0][0]

    crime_percentages = crime_details.withColumn(
        "percentage",
        F.round((crime_details['count'] / crime_details['total_count']) * 100, 2)
    ).select('area_basica_policial', 'ambit_fet', 'percentage', 'total_count').orderBy('area_basica_policial', 'percentage', ascending=False)
    
    crime_percentages_pandas = crime_percentages.toPandas()
    return crime_percentages_pandas, total_crimes_all_neighborhoods

# Helper Function: Encoding binary files to base64 for embedding images or files in HTML outputs
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Popup Content Creation: Generating dynamic HTML content for map popups based on location and review data
def popup_content_review(location_info, reviews_data, emoji):
    filtered_reviews = reviews_data.filter(reviews_data['location_id'] == location_info['location_id'])
    
    if filtered_reviews.count() == 0:
        popup_content = f"""
        <h3>{location_info['name']}</h3>
        <p><strong>🌟 Rating:</strong> {location_info['avg_rating']}</p>
        <p>No Reviews yet</p>
        """
    else:
        random_review = filtered_reviews.orderBy(rand()).limit(1).collect()[0]
        popup_content = f"""
        <h3> {emoji} {location_info['name']}</h3>
        <h4>🌟 Average Rating = {location_info['avg_rating']:.2f}</h4>
        <div style="display: flex; align-items: center;">
            <img src="{random_review['user_avatar_small']}" style="width: 50px; height: 50px; margin-right: 10px;">
            <h4>@{random_review['user_username']}</h4>
        </div>
        <p>(random reviewer)<p>
        <strong>Rating: </strong>{random_review['rating']}</p>
        <p><strong>{random_review['title']}</strong></p>
        <p><strong>Text: </strong>{random_review['text']}</p>
        """
    return popup_content

