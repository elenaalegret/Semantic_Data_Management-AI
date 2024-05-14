#################################
### Data Formatting Pipeline  ###
#################################
'''
 Description:
 This script formats and preprocesses various datasets for further analysis. 
 It involves connecting to a DuckDB database, loading data using Spark, preprocessing the data, and saving it back to DuckDB tables.

 Inputs:
 - Parquet files containing Airbnb listings, criminal dataset, TripAdvisor locations, and TripAdvisor reviews data

 Outputs:
 - DuckDB database with formatted tables for Airbnb listings, criminal dataset, TripAdvisor locations, and TripAdvisor reviews
'''

# Import
import os
import duckdb
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, array_join, concat_ws

## Prepare the DuckDB connection
con = duckdb.connect(database='./../data/formatted_zone/barcelona.db', read_only=False)
con.close()

## Spark
print('Spark Inicialitzation...')
spark = SparkSession.builder\
    .config("spark.jars", "duckdb_jdbc-0.10.1.jar") \
    .appName("DataFormatting") \
    .getOrCreate()


## Load .parquet database with spark 
print('Reading .parquet files...')
df_airbnb_listings = spark.read.parquet('./../data/landing_zone/airbnb_listings.parquet')
df_criminal_dataset = spark.read.parquet('./../data/landing_zone/criminal_dataset.parquet')
df_tripadvisor_locations = spark.read.parquet('./../data/landing_zone/tripadvisor_locations.parquet')
df_tripadvisor_reviews = spark.read.parquet('./../data/landing_zone/tripadvisor_reviews.parquet')

### As the Airbnb dataset gives us problems, we need it to make a preparatory preprocessing
#### Convert array type columns to strings separated by commas and remove the ones that can not be preprocess
# Look for array columns: df_airbnb_listings.printSchema()
df_airbnb_listings = df_airbnb_listings.withColumn("host_verifications", concat_ws(", ", col("host_verifications")))
df_airbnb_listings = df_airbnb_listings.withColumn("amenities", concat_ws(", ", col("amenities")))
df_airbnb_listings = df_airbnb_listings.withColumn("features", concat_ws(", ", col("features")))


## Write on the tables 
print('Writting tables...')
jdbc_url = 'jdbc:duckdb:./../data/formatted_zone/barcelona.db'
driver = "org.duckdb.DuckDBDriver"

print('    - Aribnb table')
df_airbnb_listings.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "df_airbnb_listings") \
    .option("driver", driver) \
    .save()

print('    - Criminal table')
df_criminal_dataset.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "df_criminal_dataset") \
    .option("driver", driver) \
    .save()

print('    - Tripadvisor Locations table')
df_tripadvisor_locations.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "df_tripadvisor_locations") \
    .option("driver", driver) \
    .save()

print('    - Tripadvisor Reviews table')
df_tripadvisor_reviews.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "df_tripadvisor_reviews") \
    .option("driver", driver) \
    .save()

spark.stop()


