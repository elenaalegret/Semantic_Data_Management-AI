
## RDF Graph Functions

# Import 
from rdflib import Literal
from rdflib.namespace import RDF, RDFS, XSD
import random

def add_criminal_instances(g, loc, inc, ex, df):
    """
    Add criminal instances to the RDF graph
        :param g: RDF graph
        :param loc: Namespace for location
        :param inc: Namespace for incident
        :param ex: Example namespace
        :param df: DataFrame containing criminal data
    """
    for idx, row in df.iterrows():
        district = loc[row["area_basica_policial"].replace(" ", "_")] # Ajusted to not have blanck spaces
        g.add((district, RDF.type, loc.District))
        g.add((district, RDFS.label, Literal(row["area_basica_policial"], datatype=XSD.string)))
        
        # Incident instance
        incident = ex[f'incident_{idx}']
        g.add((incident, RDF.type, inc.Incident))
        g.add((incident, inc.happenedAt, district))  # Relates to the district
        g.add((incident, inc.year, Literal(row['any'], datatype=XSD.integer)))
        g.add((incident, inc.numberMonth, Literal(row['num_mes'], datatype=XSD.integer)))
        g.add((incident, inc.nameMonth, Literal(row['nom_mes'], datatype=XSD.string)))
        g.add((incident, inc.typePenalCode, Literal(row['tipus_de_fet_codi_penal'], datatype=XSD.string)))
        g.add((incident, inc.wherePenalCode, Literal(row['tipus_de_lloc_dels_fets'], datatype=XSD.string)))
        g.add((incident, inc.incidentType, Literal(row['ambit_fet'], datatype=XSD.string)))
        g.add((incident, inc.numberVictims, Literal(row['nombre_victimes'], datatype=XSD.float)))
        break

def add_airbnb_instances(g, apt, df):
    """
    Add Airbnb instances to the RDF graph
        :param g: RDF graph
        :param apt: Namespace for apartment
        :param df: DataFrame containing Airbnb data
    """
    for idx, row in df.iterrows():
        apartment = apt[f'apartment_{idx}']
        g.add((apartment, RDF.type, apt.Apartment))
        g.add((apartment, apt.criminalityIndex, Literal(row['criminality_index'], datatype=XSD.float)))
        g.add((apartment, apt.extraPeople, Literal(row['extra_people'], datatype=XSD.integer)))
        g.add((apartment, apt.propertyType, Literal(row['property_type'], datatype=XSD.string)))
        g.add((apartment, apt.roomType, Literal(row['room_type'], datatype=XSD.string)))
        g.add((apartment, apt.accommodates, Literal(row['accommodates'], datatype=XSD.integer)))
        g.add((apartment, apt.bathrooms, Literal(row['bathrooms'], datatype=XSD.integer)))
        g.add((apartment, apt.bedrooms, Literal(row['bedrooms'], datatype=XSD.integer)))
        g.add((apartment, apt.beds, Literal(row['beds'], datatype=XSD.integer)))
        g.add((apartment, apt.bedType, Literal(row['bed_type'], datatype=XSD.string)))
        g.add((apartment, apt.price, Literal(row['price'], datatype=XSD.float)))
        g.add((apartment, apt.securityDeposit, Literal(row['security_deposit'], datatype=XSD.float)))
        g.add((apartment, apt.cleaningFee, Literal(row['cleaning_fee'], datatype=XSD.float)))
        g.add((apartment, apt.guestsIncluded, Literal(row['guests_included'], datatype=XSD.integer)))
        g.add((apartment, apt.cancellationPolicy, Literal(row['cancellation_policy'], datatype=XSD.string)))
        #g.add((apartment, apt.reviewScoresLocation, Literal(row['review_scores_location'], datatype=XSD.integer)))
def add_entertainment_instances(g, ent, df, identifier):
    """
    Add entertainment instances to the RDF graph
        :param g: RDF graph
        :param ent: Namespace for entertainment
        :param df: DataFrame containing entertainment data
        :param identifier: Unique identifier to differentiate instances from different DataFrames
    """
    for idx, row in df.iterrows():
        entertainment = ent[f'entertainment_{identifier}_{idx}']
        g.add((entertainment, RDF.type, ent.Entertainment))
        g.add((entertainment, ent.name, Literal(row['name'], datatype=XSD.string)))
        g.add((entertainment, ent.adress, Literal(row['address_obj_address_string'], datatype=XSD.string)))
        g.add((entertainment, ent.typeEnt, Literal(row['type'], datatype=XSD.string)))


def print_random_instance(g, class_type):
    """
    Objective: Print a random instance of a given class from the RDF graph
        :param g: RDF graph
        :param class_type: RDF class type to filter instances
    """
    instances = list(g.subjects(RDF.type, class_type))
    if not instances:
        print(f"No instances of type {class_type} found in the graph.")
        return
    
    random_instance = random.choice(instances)
    print(f"\nRandom instance of type {class_type}: {random_instance}")
    for s, p, o in g.triples((random_instance, None, None)):
        print(f"  {p.split('/')[-1]}: {o}")