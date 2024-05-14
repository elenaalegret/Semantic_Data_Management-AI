###########################################
##         Airbnb Listings Dataset       ##
##             Preparation               ##
###########################################
'''
 Description:
 This script retrieves a dataset containing Airbnb listings for analysis. 
 It utilizes the OpenDataSoft API to fetch data specifically for Barcelona. 
 The retrieved data is then processed and saved in Parquet format for further analysis.

 Inputs:
    - None

 Outputs:
    - A Parquet file containing the Airbnb listings dataset for Barcelona.
'''

# Importing necessary libraries
import pandas as pd
import requests
import io

# Making API request to load the entire dataset
total_results = []
start = 0
rows = 100
while start < 10000:
    # Incrementing by 100: &start=0&rows=100 ...
    # Filtering specifically for Barcelona and ensuring the summary variable is not NULL
    response = requests.get(f'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/airbnb-listings/records?where=city%20like%20%22Barcelona%22%20and%20summary%20is%20not%20null&start={start}&limit={rows}').json()
    total_count = response['total_count']
    results_normalized = pd.json_normalize(response, 'results')
    total_results.append(results_normalized)
    start += rows

# Combining all requests into one
airbnb_listings = pd.concat(total_results, ignore_index=True)
airbnb_listings.to_parquet('./../data/landing_zone/airbnb_listings.parquet')

