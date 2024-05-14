###########################################
##  TripAdvisor Reviews Data Retrieval   ##
###########################################

## Description:
## This script retrieves reviews data for locations from TripAdvisor's API based on location IDs obtained from the TripAdvisor locations dataset. 
## It fetches reviews for each location and stores them in a DataFrame. 
## The retrieved data is then saved in Parquet format for further analysis.

## Inputs:
## - Parquet file containing TripAdvisor locations data

## Outputs:
## - Parquet file containing TripAdvisor reviews data

# Imports
import pandas as pd
import requests
import ast
import time

# Read TripAdvisor locations data from Parquet file
tripadvisor = pd.read_parquet("./../data/landing_zone/tripadvisor_locations.parquet")

total_results = []
count = 0

print(tripadvisor.shape)
# Search for restaurant reviews
for i, info in tripadvisor.iterrows():

    url = f'https://api.content.tripadvisor.com/api/v1/location/{info["location_id"]}/reviews?key=87F2BA22551E40B69B57254881723D6E&language=en&limit=80'

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        
        print(count)

        response = response.json()
        db = pd.json_normalize(response['data'])
        total_results.append(db)

        count += 1
    
    #Per asseguar-se de no accedir el límit per segon de TripAdvisor
    time.sleep(0.2)

tripadvisor_reviews = pd.concat(total_results, ignore_index=True)
# Save the DataFrame as Parquet file
tripadvisor_reviews.to_parquet('./../data/landing_zone/tripadvisor_reviews.parquet')
