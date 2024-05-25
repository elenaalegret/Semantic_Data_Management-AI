###################################
##     Data Explotation Zone     ##
###################################
 
"""
EXPLICACIÓ
"""

# Imports
import rdflib # Handle RDF(S) data, generating triples, posing sparql queries, etc.
import sqlite3
from SPARQLWrapper import SPARQLWrapper, JSON, RDFXML, TURTLE, CSV # Generate and execute SPARQL query over the SPARQL endpoint.
from rdflib.namespace import FOAF, XSD, RDF, RDFS # Most common namespaces 
import urllib.parse # Parse strings to URI's
import networkx as nx
from pyvis.network import Network

# Connect to the DuckDB database 
conn = sqlite3.connect('../data/trusted_zone/barcelona_processed.db')
cursor = conn.cursor()

# Obtain the table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()


for table in tables: 
    table_name = table[0]
    print(f"\nTabla: {table_name}")
    
    # Obtener solo tres filas de la tabla
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
    rows = cursor.fetchall()

    # Obtener los nombres de las columnas
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]

    # Procesar las filas y columnas
    for row in rows:
        data = dict(zip(columns, row))
        print(data)

conn.close()


""""
EXAMPLE OF INSTANCE DEFINITION
location_uri = ex['Location1']
entertainment_uri = ex['Entertainment1']
apartment_uri = ex['Apartment1']

g.add((location_uri, RDF.type, loc.Locations))
g.add((entertainment_uri, RDF.type, ent.Entertainment))
g.add((apartment_uri, RDF.type, apt.Apartment))

"""