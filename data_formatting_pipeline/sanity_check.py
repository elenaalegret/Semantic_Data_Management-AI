#############################
## Formatting Sanity Check ##
#############################

## Description:
## This script performs a sanity check on the contents of the formatted database. 
## It connects to the DuckDB database containing the formatted tables and checks the number of records 
## in each table, as well as provides a preview of the first 5 rows of each table for verification.

## Imports
import duckdb

def check_database_contents():
    """
    Objective: Check the contents of the formatted database.
    """
    # Connect to the database
    con = duckdb.connect(database='./../data/formatted_zone/barcelona.db', read_only=True)
    
    try:
        # List of tables to check
        tables = ['df_airbnb_listings', 'df_criminal_dataset', 'df_tripadvisor_locations', 'df_tripadvisor_reviews']
        
        for table in tables:
            # Count the number of records in each table
            count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchall()
            print(f"Number of records in {table}: {count[0][0]}")
            
            # Show the first 5 rows of each table for verification
            preview = con.execute(f"SELECT * FROM {table} LIMIT 5").fetchdf()
            print(f"Preview of data in {table}:")
            print(preview)
    
    finally:
        # Make sure to close the connection
        con.close()

## Perform the sanity check
check_database_contents()
