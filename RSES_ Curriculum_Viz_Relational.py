import pandas as pd
from graphviz import Digraph
import random

# Load cluster/node data from sheet "Nodes"
excel_file = 'Curriculum_Data.xlsx'
nodes_df = pd.read_excel(excel_file, sheet_name='Nodes')

# Load relationship (lecture title relationships) data from sheet "Relationships"
relationships_df = pd.read_excel(excel_file, sheet_name='Relationships')

# Load cluster relationship (pre-requisities) data from sheet "Relationships"
cluster_relationships_df = pd.read_excel(excel_file, sheet_name='Cluster Relationships')

dot = Digraph()
dot.attr(fontname='Helvetica, Arial, sans-serif')
dot.attr('node', fontname='Helvetica, Arial, sans-serif', shape='rectangle', style='filled', color='white')
dot.attr('edge', fontname='Helvetica, Arial, sans-serif')
#dot.attr(rankdir='TB')  # Set rank direction to top to bottom
#dot.attr(rank='source')  # Set rank for the entire graph
dot.attr(concentrate = 'true')

start_node = 'EMSC Undergraduate Program'
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

                # Exclude cluster name from node_list (breaks layout)
                #node_list = [node for node in node_list if node != cluster]

                if node_list:
                        dot.edge(invisible_node, node_list[0], style='invis')

                # Create edges based on node names within the cluster
                c.edges([(str(node_list[j]), str(node_list[j+1])) for j in range(len(node_list) - 1) if node_list[j] and node_list[j+1]])

                # Get first node to bold & circle
                if node_list:
                  first_node = node_list[0]
                  dot.node(first_node, border="1", shape='rectangle', fontsize="20pt", fontweight="500", style='bold', color='blue', fixedsize='true', width='3')


# Iterate through relationships and create edges
for index, row in relationships_df.iterrows():
    source = row['Source']
    target = row['Target']
    dot.edge(source, target)

# Iterate through cluster relationships and create edges
for index, row in cluster_relationships_df.iterrows():
    source_cluster = row['Source Cluster']
    target_cluster = row['Target Cluster']

    # Get node lists for source and target clusters
    source_node_list = nodes_df[nodes_df['Cluster'] == source_cluster].iloc[0].tolist()[2:]
    target_node_list = nodes_df[nodes_df['Cluster'] == target_cluster].iloc[0].tolist()[2:]

    # Find last node of source cluster and first node of target cluster
    if source_node_list and target_node_list:
        source_node = source_node_list[-1]
        target_node = target_node_list[0]

        # Create edge with directional arrow
        target_cluster_with_rank = f"{target_cluster}_{nodes_df[nodes_df['Cluster'] == target_cluster]['Rank'].iloc[0]}"
        source_cluster_with_rank = f"{source_cluster}_{nodes_df[nodes_df['Cluster'] == source_cluster]['Rank'].iloc[0]}"
        dot.edge(source_node, target_node, arrowhead='normal',  color='green', dir='forward', lhead=f"cluster_{target_cluster_with_rank}")


dot.render('Curriculum_Vis_Rel_graph', format='png', view=True)

