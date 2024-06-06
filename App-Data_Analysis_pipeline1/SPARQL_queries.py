
######################
### Data Loading   ###
######################

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, Namespace
import pandas as pd 
import streamlit as st
import base64

# Loading the explotation dataset for Data Analysis 1
#####################################################
# Load the RDF graph
g = Graph()
g.parse("./../data/explotation_zone/RDFGraph_Visualitzation.ttl", format="ttl")

# Namespaces _____________________________________
ex = Namespace('http://example.org/')
loc = Namespace('http://example.org/location/')
ent = Namespace('http://example.org/entertainment/')
apt = Namespace('http://example.org/apartment/')
inc = Namespace('http://example.org/incident/')
schema = Namespace('http://schema.org/')

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
##      Queries Functions     ###
#################################

def filter_apartments(neighborhoods, price_max=None, selected_room_types=None, bathrooms_min=None, beds_min=None, min_nights=None, num_samples=None):
    #  SPARQL dynamic query
    query = """
    PREFIX apt: <http://example.org/apartment/>
    PREFIX loc: <http://example.org/location/>

    SELECT ?apartment ?name ?district ?price ?room_type ?bathrooms ?beds ?minimum_nights ?bed_type ?latitude ?longitude
    WHERE {
        ?apartment apt:hasLocation ?location .
        ?apartment apt:name ?name .
        ?location loc:isinDistrict ?district .
        ?apartment apt:bedType ?bed_type .
        ?apartment apt:price ?price .
        ?apartment apt:roomType ?room_type .
        ?apartment apt:bathrooms ?bathrooms .
        ?apartment apt:beds ?beds .
        ?apartment apt:minimumNights ?minimum_nights .
        ?location loc:Latitude ?latitude .
        ?location loc:Longitude ?longitude .
    """
    
    if neighborhoods is not None:
        selected_neighborhoods = [neigh for neigh, selected in neighborhoods.items() if selected]
        if selected_neighborhoods:
            neighborhoods_filter = " || ".join([f'?district = loc:{neigh.replace(" ", "_")}' for neigh in selected_neighborhoods])
            query += f"FILTER ({neighborhoods_filter}) .\n"
        else:
            query += "FILTER (?beds = 1000) .\n"  # Impossible filter

    if price_max is not None:
        query += f"FILTER (?price <= {price_max}) .\n"

    if selected_room_types is not None:
        room_types_filter = " || ".join([f'?room_type = "{rt}"' for rt in selected_room_types])
        query += f"FILTER ({room_types_filter}) .\n"

    if bathrooms_min is not None:
        query += f"FILTER (?bathrooms >= {bathrooms_min}) .\n"

    if beds_min is not None:
        query += f"FILTER (?beds >= {beds_min}) .\n"

    if min_nights is not None:
        query += f"FILTER (?minimum_nights >= {min_nights}) .\n"

    query += "}"
    
    results = g.query(query)

    # For injecting the data in folium map -> We need a tabular format
    df_filtered_apartments = pd.DataFrame(results, columns=results.vars)
    
    if num_samples:
      # In case of wanting more resources change 1000 to 100
      df_filtered_apartments = df_filtered_apartments.sample(frac=num_samples/1000, random_state=42)

    df_filtered_apartments.columns = df_filtered_apartments.columns.str.strip()

    return df_filtered_apartments


def filter_locations(neighborhoods, min_rating=None, num_samples=None):
    #  SPARQL dynamic query
    query = """
    PREFIX ent: <http://example.org/entertainment/>
    PREFIX loc: <http://example.org/location/>

    SELECT ?location_id ?name ?location ?type ?district ?latitude ?longitude ?avgrating
    WHERE {
        ?entertainment ent:locationID ?location_id .
        ?entertainment ent:name ?name .
        ?entertainment ent:typeEnt ?type .
        ?entertainment ent:avgrating ?avgrating .
        ?entertainment ent:hasLocation ?location .
        ?location loc:latitude ?latitude .
        ?location loc:longitude ?longitude .
        ?location loc:isinDistrict ?district .
    """

    selected_neighborhoods = [neigh for neigh, selected in neighborhoods.items() if selected]
    if selected_neighborhoods:
        neighborhoods_filter = " || ".join([f'?district = loc:{neigh.replace(" ", "_")}' for neigh in selected_neighborhoods])
        query += f"FILTER ({neighborhoods_filter}) .\n"
    
    else:
        query += "FILTER (?isinDistrict = 0) .\n"  # Impossible filter


    if min_rating is not None:
        query += f"FILTER (?avgrating >= {min_rating}) .\n"

    query += "}"
    
    results = g.query(query)
 
    df_filtered_locations = pd.DataFrame(results, columns=results.vars)

    if num_samples:
        df_filtered_locations = df_filtered_locations.sample(frac=num_samples / 100, random_state=42)

    df_filtered_locations.columns = df_filtered_locations.columns.str.strip()
    df_filtered_locations['type'] = df_filtered_locations['type'].apply(lambda x: str(x))
    return df_filtered_locations



# Helper Function: Encoding binary files to base64 for embedding images or files in HTML outputs
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def popup_content_review(id, emoji, name, avg_rating):
    # Construir la consulta SPARQL
    query = f"""
    PREFIX ent: <http://example.org/entertainment/>
    PREFIX loc: <http://example.org/location/>

    SELECT ?locationid ?rating ?text ?title 
    WHERE {{
        ?entertainment ent:locationID ?locationid .
        ?entertainment ent:rating ?rating .
        ?entertainment ent:text ?text .
        ?entertainment ent:title ?title .
        FILTER(?locationid = {id}) .
    }}
    LIMIT 1
    """
  
    results = g.query(query)
    results = pd.DataFrame(results, columns=results.vars)
    results.columns = results.columns.str.strip()

    review = results.iloc[0]
    popup_content = f"""
    <h3> {emoji} {name}</h3>
    <h4>🌟 Average Rating = {avg_rating}</h4>

    <p>(👤 Random Reviewer)<p>
    <strong>Rating: </strong>{review['rating']}</p>
    <p><strong>💬 {str(review['title'])}</strong></p>
    <p><strong>Text: </strong>{str(review['text'])}</p>
    """
   
    return popup_content





