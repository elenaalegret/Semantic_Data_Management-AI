# Create the knowledge graph

#pip install torchkge

# Import
from torchkge.data_structures import KnowledgeGraph
from rdflib import Graph
import pandas as pd
import trainer
import os


# Load the RDF graph
g = Graph()
g.parse("./../data/explotation_zone/RDFGraph.ttl", format="ttl")

# Extract triples in order to create the Knowledge graph
print('Creating the triples...')
triples = []
for s, p, o in g:
    triples.append((str(s), str(p), str(o)))

directory = './../data/explotation_zone'  # Cambia esto a la ruta deseada
os.makedirs(directory, exist_ok=True)
file_path = os.path.join(directory, 'RDFTriples.txt')

# Save triples into a file
with open(file_path, 'w') as f:
    for triple in triples:
        f.write("\t".join(triple) + "\n")
print('Done!')
print()

        
print('Creating the Knowledge graph...')
# Convert into DataFrame and reorganize col to torchKGE format
data = pd.DataFrame(triples, columns=['from', 'rel', 'to'])
data = data[['from', 'to', 'rel']]

# Map entities and relations into indexes
entities = list(set(data['from']).union(set(data['to'])))
relations = list(set(data['rel']))

entity2id = {entity: idx for idx, entity in enumerate(entities)}
relation2id = {relation: idx for idx, relation in enumerate(relations)}

# Apply mapping to data 
data['from'] = data['from'].map(entity2id)
data['to'] = data['to'].map(entity2id)
data['rel'] = data['rel'].map(relation2id)

# Split data into training, validation, and test sets
train_ratio, val_ratio, test_ratio = 0.8, 0.1, 0.1
assert train_ratio + val_ratio + test_ratio == 1.0, "Ratios must sum to 1"

n = len(data)
train_end = int(train_ratio * n)
val_end = int((train_ratio + val_ratio) * n)

train_data = data.iloc[:train_end]
val_data = data.iloc[train_end:val_end]
test_data = data.iloc[val_end:]

# Create KnowledgeGraph
kg_train = KnowledgeGraph(df=train_data)
kg_val = KnowledgeGraph(df=val_data)
kg_test = KnowledgeGraph(df=test_data)
print('Done!')
print()

# Start training
print('Starting the training...')
trainer.train_model(kg_train, kg_val)