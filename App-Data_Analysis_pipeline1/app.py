##################################
### Map4Tourism - Tourism Tool ###
##########################################################################################################################################################################

# BCN Map4Tourism is a comprehensive tourism tool designed to enhance the experience of visitors to Barcelona. 
# 
# Key Features:
# - Dynamic Map Visualization: Utilizes Folium to plot interactive maps showcasing Airbnb listings, restaurants, 
#                              and other attractions with custom markers based on user selections.
# - Data-Driven Insights: Offers a filtering system for selecting neighborhoods and attractions based on user preferences, including ratings and types of establishments.
# - Responsive Interface: Built with Streamlit, the tool includes a custom header with a logo, sidebar configurations for neighborhood selection, 
#                         and sliders for customizing data representation.
##########################################################################################################################################################################

# Imports
import folium
from streamlit_folium import folium_static
import numpy as np
from SPARQL_queries import *

# Header section: Displays a custom header with a logo and main title on the Streamlit app
st.write("""
    <div style="display:flex;align-items:center;">
        <img src="data:image/png;base64,{}" width="110">
        <h1 style="margin-left:10px;">BCN Map4Tourism</h1>
    </div>
""".format(get_base64_of_bin_file("images/logo.png")), unsafe_allow_html=True)
st.write("Welcome! Choose your neighborhood 🏘️ and explore local restaurants alongside crime rate \n statistics for a more informed experience. 😊🍽️📊")

#################################
##   Sidebar configuration    ###
#################################

# --> Allows users to select different neighborhoods and options for visualization 
selected_neighborhoods = {}
with st.sidebar.expander("Neighborhoods"):
    col1, col2 = st.columns([2, 1])
    for neighborhood, color in colors.items():
        is_selected = col1.checkbox(f"{neighborhood}", key=f"chk_{neighborhood}")
        selected_neighborhoods[neighborhood] = is_selected
        col2.markdown(f"<span style='display: inline-block; width: 12px; height: 12px; background: {color}; margin-left: 10px;'></span>", unsafe_allow_html=True)


# !!!!!!Attention!!!!!_____________________________________________________________________________________
# Limited computational resources may restrict rendering capabilities locally
# Additional resources would enable processing of larger datasets.
# --> Less apartments for visualization in local:  num_samples/1000 -- only 10% of the total data
# --> If you have resources comment the indicated line
#__________________________________________________________________________________________________________

# Data sampling and filtering: Reduces dataset based on user-selected percentage for performance optimization
num_samples = st.sidebar.slider("Percentage of Locations Displayed", min_value=1, max_value=100, value=20)

with st.sidebar.expander(" 🧹 Apartments Filtration"):
    price_max = st.sidebar.slider("💰 Maximum Price per Night", min_value=0, max_value=1000, value=80)
    more_filters_active = st.sidebar.checkbox("More Filtration")
    if more_filters_active:
        room_types = ['Entire home/apt', 'Private room', 'Shared room']  
        selected_room_types = st.sidebar.multiselect("Room Types", room_types, default=room_types)
        bathrooms_min = st.sidebar.slider("Minimum Bathrooms", min_value=0, max_value=5, value=0)
        beds_min = st.sidebar.slider("Minimum Beds", min_value=0, max_value=11, value=0)
        min_nights = st.sidebar.slider("Minimum Nights", min_value=0, max_value=365, value=0)
    else:
        selected_room_types = None
        bathrooms_min = None
        beds_min = None
        min_nights = None

# -->  Call the query fucntion for Apartments
df_filtered_apartments = filter_apartments(selected_neighborhoods, price_max, selected_room_types, bathrooms_min, beds_min, min_nights, num_samples)


# Display the number of apartments & Locations
st.markdown(f'''
<div style="
    border-radius: 10px;
    border: 2px solid #ff9832;
    padding: 15px;
    margin-top: 5px;
    margin-bottom: 5px;
    font-size: 16px;
    color: #ff9832;
    background-color: #ffffff;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.1);">
    <b> Displayed Apartments </b> {df_filtered_apartments.shape[0]}
</div>
''', unsafe_allow_html=True)


#################################
##      Map visualization.    ###
#################################
#  Configures and displays a map with markers for Airbnb listings and optionally restaurants/attractions
show_restaurants_attractions = st.checkbox("Show Restaurants & Attractions") # Choose to see restaurants_attractions

m = folium.Map(location=[41.3879, 2.1699], zoom_start=12)
if show_restaurants_attractions:

    min_rating = st.slider("🧹 Filter by Minimum Rating", min_value=0, max_value=5, value=5)

    # -->  Call the query fucntion for Locations
    filtered_locations = filter_locations(selected_neighborhoods, min_rating, num_samples)
    
    # Adds markers for restaurants and attractions to the map
    for _, row in filtered_locations.iterrows():
        neighbourhood = str(row['district']).split('/')[-1].replace('_', ' ')
        emoji = "🍽️" if row['type'] == "restaurant" else "📌"
        popup_content = popup_content_review(row['location_id'], emoji, row['name'], row['avgrating'])
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_content, max_width=600),  # Popup con nombre y tipo
            tooltip=f"{emoji} {row['type']} ",
            icon=folium.Icon(color=colors.get(neighbourhood, 'gray'), icon=location_icons.get(row['type']))
        ).add_to(m)

    st.markdown(f'''
    <div style="
        border-radius: 10px;
        border: 2px solid #a26464;
        padding: 15px;
        margin-top: 5px;
        margin-bottom: 5px;
        font-size: 16px;
        color: #a26464;
        background-color: #ffffff;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);">
        <b>Displayed Restaurants </b> {filtered_locations[filtered_locations['type'] == 'restaurant'].shape[0]}<br>
        <b>Displayed Attractions </b> {filtered_locations[filtered_locations['type'] == 'attraction'].shape[0]}
    </div>
    ''', unsafe_allow_html=True)

for _, row in df_filtered_apartments.iterrows():
    neighbourhood = row['district'].split('/')[-1].replace('_', ' ')
    marker_color = colors.get(neighbourhood, 'gray')
    description = f"🏠 {row['room_type']}\n\nPrice {row['price']} €"

    popup_content = f"""
        <p>🏠 {row['name']}</p>
        <b>💲 Price: {row['price']} €</b><br>
        <p>🚽 Bathrooms: {row['bathrooms']}</p>
        <p>🛌 Beds: {row['beds']}</p>
        <p>➡️ Type: {row['bed_type']}</p>
    """

    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=f"{description}",
        icon=folium.Icon(color=marker_color, icon='home', prefix='fa')
    ).add_to(m)

# Show the map
folium_static(m)









