
## RDF Graph Functions

# Import 
from rdflib import Literal
from rdflib.namespace import RDF, RDFS, XSD
import random
import networkx as nx
from rdflib.namespace import RDF, RDFS
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import unidecode

# ------------------------ Functions used in the Quality Pipeline ------------------------
def plot_numeric_histograms(df, numeric_columns):
    colors = ['skyblue', 'salmon', 'lightgreen', 'orange']
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))  
    axs = axs.flatten()  
    
    for i, column in enumerate(numeric_columns):
        column_data = df.select(column).rdd.flatMap(lambda x: x).collect()

        if column_data:
            ax = axs[i] 
            frequencies, bins, _ = ax.hist(column_data, bins=20, color=colors[i], edgecolor='black')
            ax.set_title(f'Histogram of {column}')
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) 
    plt.tight_layout()
    plt.show()

def plot_categorical_distribution(df, column, ax, color):
    counts = df.groupBy(column).count().orderBy(column).collect()
    labels = [row[column] for row in counts]
    frequencies = [row['count'] for row in counts]
    ax.bar(labels, frequencies, color=color)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of {column}')
    ax.tick_params(axis='x', rotation=90)

def generate_word_cloud(values, title):
    text = " ".join(value.lower() for value in values) # Unifquem en minuscuels y sense accents x treure + insides
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    plt.show()







# ------------------------ Functions used in the Explotation Pipeline ------------------------
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


def visualize_rdf_graph(g, output_file="./..data/explotation_zone/rdf_schema.png"):
    """
    Visualizes an RDF graph using NetworkX and matplotlib.
        :param g: rdflib.Graph, the RDF graph to visualize
        :param output_file: str, the path to save the output image
    """
    # Create a NetworkX graph for visualization
    nx_graph = nx.DiGraph()
    print('It is important to ensure that the visualization will be rendered correctly only \
           if there are no instances added and the graph remains simple.')

    # Add nodes and edges to the NetworkX graph based on the schema with specific levels
    for s, p, o in g:
        if p == RDF.type and o == RDFS.Class:
            if str(s).split('/')[-1] == 'Locations':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=1)
            elif str(s).split('/')[-1] in ['Apartment', 'Entertainment']:
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=2)
            elif str(s).split('/')[-1] in ['Incident', 'District']:
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=6)
        elif p == RDFS.subClassOf:
            nx_graph.add_edge(o, s, label='rdf:subClassOf')
        elif p == RDFS.domain:
            if str(s).split('/')[-1] in ['isinDistrict', 'Latitude', 'Longitude']:
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=3)
            elif str(s).split('/')[-1] == 'happened_at':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=5)
            elif str(s).split('/')[-1] == 'incidentType':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=7)
            nx_graph.add_edge(o, s, label='rdf:domain')
        elif p == RDFS.range:
            nx_graph.add_edge(s, o, label='rdf:range')
        elif isinstance(o, Literal):
            literal_label = f'"{o}"^^{o.datatype.split("#")[-1]}'
            nx_graph.add_node(o, label=literal_label, level=10)
            nx_graph.add_edge(s, o, label='rdf:'+str(p).split('/')[-1])

    # Ensure all nodes have a label and level
    for n in nx_graph.nodes():
        if 'label' not in nx_graph.nodes[n]:
            nx_graph.nodes[n]['label'] = str(n).split('/')[-1].split('#')[-1]
        if 'level' not in nx_graph.nodes[n]:
            nx_graph.nodes[n]['level'] = 5

    # Generate node positions using the 'dot' layout
    pos = graphviz_layout(nx_graph, prog='dot')

    # Adjust positions to order descending levels
    for node, coords in pos.items():
        level = nx_graph.nodes[node]['level']
        pos[node] = (coords[0], -level)

    # Draw the graph using matplotlib
    plt.figure(figsize=(20, 12))
    nx.draw(nx_graph, pos, with_labels=True, labels={n: d['label'] for n, d in nx_graph.nodes(data=True)},
            node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels={(u, v): d['label'] for u, v, d in nx_graph.edges(data=True)})

    # Save the image to a file
    plt.savefig(output_file, format="PNG")

    # Show the image
    plt.show()


def visualize_hierarchical_rdf_graph(g, output_file="./..data/explotation_zone/rdf_schema_hierarchical_levels_ordered_spaced.png"):
    """
    Visualizes an RDF graph using NetworkX and matplotlib.
        :param g: rdflib.Graph, the RDF graph to visualize
        :param output_file: str, the path to save the output image
    """
    # Create a NetworkX graph for visualization
    nx_graph = nx.DiGraph()
    print('It is important to ensure that the visualization will be rendered correctly only \
           if there are no instances added and the graph remains simple.')
    
    # Add nodes and edges to the NetworkX graph based on the schema with specific levels
    for s, p, o in g:
        if p == RDF.type and o == RDFS.Class:
            if str(s).split('/')[-1] == 'Locations':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=1)
            elif str(s).split('/')[-1] in ['Apartment', 'Entertainment']:
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=2)
            elif str(s).split('/')[-1] == 'District':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=3)
            elif str(s).split('/')[-1] == 'Incident':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=4)
        elif p == RDFS.subClassOf:
            nx_graph.add_edge(o, s, label='rdf:subClassOf')
        elif p == RDFS.domain:
            if str(s).split('/')[-1] in ['isinDistrict', 'Latitude', 'Longitude']:
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=3)
            elif str(s).split('/')[-1] == 'happened_at':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=4)
            elif str(s).split('/')[-1] == 'incidentType':
                nx_graph.add_node(s, label=str(s).split('/')[-1], level=5)
            nx_graph.add_edge(o, s, label='rdf:domain')
        elif p == RDFS.range:
            nx_graph.add_edge(s, o, label='rdf:range')
        elif isinstance(o, Literal):
            literal_label = f'"{o}"^^{o.datatype.split("#")[-1]}'
            nx_graph.add_node(o, label=literal_label, level=5)
            nx_graph.add_edge(s, o, label='rdf:'+str(p).split('/')[-1])

    # Ensure all nodes have a label and level
    for n in nx_graph.nodes():
        if 'label' not in nx_graph.nodes[n]:
            nx_graph.nodes[n]['label'] = str(n).split('/')[-1]
        if 'level' not in nx_graph.nodes[n]:
            nx_graph.nodes[n]['level'] = 5

    # Generate node positions using the 'dot' layout with smaller rank separation
    pos = graphviz_layout(nx_graph, prog='dot', args='-Granksep=0.2')

    # Draw the graph using matplotlib
    plt.figure(figsize=(20, 12))
    nx.draw(nx_graph, pos, with_labels=True, labels={n: d['label'] for n, d in nx_graph.nodes(data=True)},
            node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels={(u, v): d['label'] for u, v, d in nx_graph.edges(data=True)})

    # Save the image to a file
    plt.savefig(output_file, format="PNG")

    # Show the image
    plt.show()