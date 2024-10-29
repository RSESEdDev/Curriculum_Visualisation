import pandas as pd
from graphviz import Digraph
import random
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import getpass
import os
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

secret = getpass.getpass('Enter your API key:')


excel_file = 'Curriculum_Data_Geology.xlsx'
csv_file ='geoBERT_text.csv'
nodes_df = pd.read_excel(excel_file, sheet_name='Nodes')
label_df = pd.read_csv(csv_file)
cluster_relationships_df = pd.read_excel(excel_file, sheet_name='Cluster Relationships')

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

exclude_words = ["Overview", "L", "Exam", r'\bEMSC\w*\b', "Poster"]  # Add wildcard pattern

def exclude_words_from_text(text, exclude_words):
    for word_or_pattern in exclude_words:
        if isinstance(word_or_pattern, str) and not word_or_pattern.startswith(r'\b'):
            # Treat as a literal word, create a regex pattern for whole word matching
            pattern = r'\b' + re.escape(word_or_pattern) + r'\b'  
            text = re.sub(pattern, '', text)
        else:
            # Treat as a regex pattern directly
            text = re.sub(word_or_pattern, '', text)
    return text

def get_embeddings_batch(texts, batch_size=16, exclude_words=[]): 
  # If 'texts' is a single string, convert it to a list
  if isinstance(texts, str) or isinstance(texts, int) or isinstance(texts, np.int32):
        texts = [str(texts)]  # Convert to list and ensure string type
  embeddings_list = []
  
  for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        modified_texts = [exclude_words_from_text(text, exclude_words) for text in batch_texts]
        if not any(modified_texts):  
            print("Warning: Empty text found in batch. Returning zero vector.")
            # Return a zero vector of the appropriate dimension
            return torch.zeros(1, model.config.hidden_size) 
        
        inputs = tokenizer(modified_texts, return_tensors='pt', padding=True, truncation=True)

        with torch.no_grad():
            outputs = model(**inputs)
        
        batch_embeddings = outputs.last_hidden_state.mean(dim=1)
        embeddings_list.append(batch_embeddings)

  # Check if embeddings_list is empty due to all batches being empty
  if not embeddings_list:
      print("Warning: All batches resulted in empty texts. Returning zero vector.")
      return torch.zeros(1, model.config.hidden_size)

  return torch.cat(embeddings_list, dim=0)

dot = Digraph()
dot.attr(fontname='Helvetica, Arial, sans-serif')
dot.attr('node', fontname='Helvetica, Arial, sans-serif', shape='rectangle', style='filled', color='white')
dot.attr('edge', fontname='Helvetica, Arial, sans-serif')
#dot.attr(rankdir='TB')  # Set rank direction to top to bottom
#dot.attr(rank='source')  # Set rank for the entire graph
dot.attr(concentrate = 'true')

start_node = 'EMSC Undergraduate Program - Geology Relationships'
dot.node(start_node, color="white", fontsize="60pt")

# Create an invisible node above the group 1 clusters
invisible_node = 'invisible_group1'
dot.node(invisible_node, style='invis', width='0', height='0')

clusters = nodes_df['Cluster'].unique()
colors = ['#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(clusters))]

# Define the desired cluster groupings based on EMSCxxxx pattern
cluster_groups = [
    [f"{cluster}_{nodes_df[nodes_df['Cluster'] == cluster]['Rank'].iloc[0]}"
     for cluster in nodes_df['Cluster'].unique() if cluster.startswith('EMSC1')],
    [f"{cluster}_{nodes_df[nodes_df['Cluster'] == cluster]['Rank'].iloc[0]}"
     for cluster in nodes_df['Cluster'].unique() if cluster.startswith('EMSC2')],
    [f"{cluster}_{nodes_df[nodes_df['Cluster'] == cluster]['Rank'].iloc[0]}"
     for cluster in nodes_df['Cluster'].unique() if cluster.startswith('EMSC3')],
    # ... add more groups as needed
]

for i, group in enumerate(cluster_groups):
    with dot.subgraph(name=f'group_{i + 1}') as g:
        previous_invisible_node = None
        for j, cluster_with_rank in enumerate(group):
            cluster, rank = cluster_with_rank.split('_')
            with dot.subgraph(name=f'cluster_{cluster_with_rank}') as c: # Use original cluster name for subgraph
                #c.attr(label=f'<<B>{cluster}</B>>')
                c.attr(color=colors[i])
                c.attr(margin='10')
                c.attr(nodesep='1.6')
                c.attr(align='center')

                # Create an invisible node within the cluster
                invisible_node = f'invisible_{cluster}'
                dot.node(invisible_node, style='invis', width='0', height='0')

                # Connect previous invisible node to current invisible node
                if previous_invisible_node:
                  dot.edge(previous_invisible_node, invisible_node, style='invis')
                previous_invisible_node = invisible_node

                # Get node names from DataFrame columns
                if (nodes_df['Cluster'] == cluster).any():  # Use original cluster name
                  node_list = nodes_df[nodes_df['Cluster'] == cluster].iloc[0].tolist()[2:]

                if node_list:
                        dot.edge(invisible_node, node_list[0], style='invis')

                # Create edges based on node names within the cluster
                c.edges([(str(node_list[j]), str(node_list[j+1])) for j in range(len(node_list) - 1) if node_list[j] and node_list[j+1]])

                # Get first node to bold & circle
                if node_list:
                  first_node = node_list[0]
                  dot.node(first_node, border="1", shape='rectangle', fontsize="20pt", fontweight="500", style='bold', color='blue', fixedsize='true', width='3')

label_mapping = {
    0: 'Earth Structure and Composition',
    1: 'Plate Tectonics and Boundaries',
    2: 'Seismology',
    3: 'Geochemistry',
    4: 'Structural Geology',
    5: 'Volcanology',
    6: 'Sedimentology',
    7: 'Geodynamics',
    8: 'Oceanography',
    9: 'Igneous & Metamorphic Rocks',
   10: 'Heat & Convection',
   11: 'Natural Hazards',
}

# Calculate similarities between intercluster nodes
intercluster_edges = []  # List to hold similar edges
threshold = 0.85  # Similarity threshold

# Create a colormap (e.g., 'viridis')
cmap = plt.get_cmap('Paired')

texts = []  # Initialize an empty list for texts
for index, row in cluster_relationships_df.iterrows():
    source_cluster = row['Source Cluster']
    target_cluster = row['Target Cluster']

    # Get node lists for source and target clusters
    source_nodes = nodes_df[nodes_df['Cluster'] == source_cluster].iloc[0, 2:].tolist()
    target_nodes = nodes_df[nodes_df['Cluster'] == target_cluster].iloc[0, 2:].tolist()
    #print(f"Source nodes for cluster {source_cluster}: {source_nodes}")
    #print(f"Target nodes for cluster {target_cluster}: {target_nodes}")
    
    for src_node in source_nodes:
        for tgt_node in target_nodes:
            # Get embeddings and calculate similarity
            src_embedding = get_embeddings_batch(src_node)
            tgt_embedding = get_embeddings_batch(tgt_node)
            #print(f"Embedding for source node {src_node}: {src_embedding}")
            #print(f"Embedding for target node {tgt_node}: {tgt_embedding}")
            
            similarity_score = cosine_similarity(
                  src_embedding.numpy().reshape(1, -1), 
                  tgt_embedding.numpy().reshape(1, -1)
              )[0, 0]  
              
              # Check if the similarity exceeds the threshold
            if similarity_score >= threshold:
                  intercluster_edges.append((str(src_node), str(tgt_node), similarity_score))
                  texts.extend([src_node, tgt_node])  # Add nodes to texts list

legend_handles = []
for i in range(cmap.N):  # cmap.N gives the number of colors in the colormap
    color = cmap(i)  # Get the color for the current index
    category_id = list(label_mapping.keys())[list(label_mapping.values()).index(label_mapping.get(i, 'Unknown'))]  # Get the category id
    category_name = label_mapping.get(category_id, 'Unknown')  # Get the category name
    legend_handles.append(mpatches.Patch(color=color, label=category_name))  # Add to legend handles

if texts:  # Check if texts list is not empty
  embeddings_2d = get_embeddings_batch(texts).numpy()
  kmeans = KMeans(n_clusters=len(label_mapping))  # Choose the number of categories
  kmeans.fit(embeddings_2d)
  pre_labels = kmeans.labels_
  decoded_labels = [label_mapping.get(label, 'Unknown') for label in pre_labels]
else:
   print("Warning: No texts found for clustering. pre_labels and decoded_labels will be empty.")

if len(pre_labels) >= len(nodes_df):
    nodes_df['Category'] = pre_labels[:len(nodes_df)]  # Assign categories to nodes_df
else:
    print("Warning: `pre_labels` has fewer entries than `nodes_df`. Some rows will not get a category.")
    nodes_df['Category'] = pre_labels + [None] * (len(nodes_df) - len(pre_labels))

# Dynamically get columns that start with 'Nodes'
node_columns = [col for col in nodes_df.columns if col.startswith('Node') and col[4:].isdigit()]

# Combine these columns into a single 'Node' column and clean up 'nan' values
nodes_df['Node'] = nodes_df[node_columns].apply(
    lambda row: [str(x) for x in row if pd.notna(x)], axis=1
)
  # Create a mapping from nodes to their categories
node_to_category = {}
for index, row in nodes_df.iterrows():
    for node in row['Node']:
        node_to_category[node] = row['Category']

# Create edges in your graph for similar nodes
for src, tgt, similarity_score in intercluster_edges:
    src_category = node_to_category.get(src, None)
    tgt_category = node_to_category.get(tgt, None)
    if src_category is None or tgt_category is None:
        print(f"Warning: Category not found for one of the nodes ({src}, {tgt}). Skipping edge.")
        continue
    
    # Set up the edge based on similarity score
    normalized_similarity = (similarity_score - threshold) / (1 - threshold)
    edge_color = mcolors.to_hex(cmap(normalized_similarity))
    dot.edge(str(src), str(tgt), color=edge_color, style='dashed')

# Instead of dot.legend(legend_handles), create a subgraph for the legend
# Instead of dot.legend(legend_handles), create a subgraph for the legend
with dot.subgraph(name='cluster_legend') as legend_subgraph:
    legend_subgraph.attr(label='Category Legend')
    legend_subgraph.attr(labelloc='t')  # Position legend at the top

    # Create invisible nodes for legend entries and connect them with edges
    for i, handle in enumerate(legend_handles):
        legend_node_name = f'legend_node_{i}'
        # Convert the color tuple to a hexadecimal color string
        color_string = mcolors.to_hex(handle.get_facecolor()) 
        legend_subgraph.node(legend_node_name, label=handle.get_label(), style='filled', color=color_string, shape='rect')

        # Connect legend nodes with invisible edges to arrange them horizontally
        if i > 0:
            legend_subgraph.edge(f'legend_node_{i-1}', legend_node_name, style='invis')
# Create a DataFrame for the relationships
df_relate = pd.DataFrame(intercluster_edges, columns=['Source Nodes', 'Target Nodes', 'Similarity Score']) 
df_relate.to_csv('intercluster_node_relationships.csv', index=False)

# Create a DataFrame to display texts with their categories
category_df = pd.DataFrame({'Text': texts, 'Category': pre_labels, 'Cat Title': decoded_labels})
category_df.to_csv('embeddings_categories.csv', index=False)

# Render the graph
dot.render('Curriculum_Vis_Rel_BERT', format='png', view=True)
