import pandas as pd
import datetime
from graphviz import Digraph
from matplotlib.colors import to_rgb, to_hex
import matplotlib.colors as mcolors

def lighten_color(color, factor=0.5):
    # Convert color name to RGB
    rgb = mcolors.to_rgba(color)
    # Lighten the color
    lightened_rgb = [min(c + factor * (1 - c), 1.0) for c in rgb[:3]]  # Lighten only R, G, B
    return mcolors.to_hex(lightened_rgb)

def wrap_text(text, max_width):
    """Wrap text to fit within the specified width."""
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word exceeds the max width
        if len(current_line) + len(word) + 1 > max_width:  # +1 for the space
            wrapped_lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line += word + " "

    if current_line:
        wrapped_lines.append(current_line.strip())

    return '\n'.join(wrapped_lines)

# Load data from Excel
nodes_df = pd.read_excel('Curriculum_Data.xlsx', sheet_name='Nodes')

# Create Graphviz object
dot = Digraph(comment='Curriculum Visualization')
dot.attr('graph', layout='osage', pad='0.5,0.5', rankdir='TB')
dot.attr('node', shape='rect', fixedsize='True', width='1.8', height='0.95', fontname='Arial', fontsize='10', style='filled,rounded', penwidth='0.5', label='')
dot.attr('edge', fontname='Arial', fontsize='10', arrowsize='0.5')

# Group clusters by level
cluster_groups = {
    "1000 Level": nodes_df[nodes_df['Cluster'].str.contains('EMSC1')]['Cluster'].unique(),
    "2000 Level": nodes_df[nodes_df['Cluster'].str.contains('EMSC2')]['Cluster'].unique(),
    "3000 Level": nodes_df[nodes_df['Cluster'].str.contains('EMSC3')]['Cluster'].unique(),
}

# Define colors for each level (this is manually set, if 4000 level add extra row)
level_colors = {
    "1000 Level": ("yellowgreen", "yellowgreen"),  # Cluster color, first node color
    "2000 Level": ("turquoise", "turquoise"),      # Cluster color, first node color
    "3000 Level": ("lightskyblue", "lightskyblue"),    # Cluster color, first node color
}

print(cluster_groups)
# Initialize counters
current_cluster_count = 2  # Start from cluster_2
level_counter = 1  # Counter for level groups

# Create main subgraph group (cluster_1)
cluster_1 = Digraph(name='cluster_1')
cluster_1.attr(packmode='array_rtu1', color='transparent', label="")

# Create subgraph for cluster_2, which wraps everything
cluster_2 = Digraph(name='cluster_2')
cluster_2.attr(packmode='array_tu1', label="", sortv="1000")

# Loop through clusters and add them to cluster_2
for level_name, clusters in cluster_groups.items():
    sortv_level = level_counter * 1000  # Set sortv to the group level
    course_counter = 0  # Initialize course counter for this level
    # Get the colors for the current level
    cluster_color, node_color = level_colors[level_name]

    # Create subgraph for each level within cluster_3
    cluster_level = Digraph(name=f'cluster_{current_cluster_count + 1}')
    cluster_level.attr(sortv=str(sortv_level + 100), packmode='array_tu1', label="", color=cluster_color)
    
    # Create the level node for the current level
    cluster_level.node(
            f"{level_counter}000_Level",  # Unique level label
            label=f"<<b>{level_name}</b>>",
            shape='rect',
            pad="0.25,0.25",
            height='0.5',
            width=f'{len(clusters)*2}',
            fillcolor=node_color,
            penwidth='0.5',
            fontname='Arial',
            fontsize='15',
            style='filled',
            labelloc='c'
        )
    current_cluster_count += 1
    
    # Create a subgraph for the clusters within this level
    cluster_4 = Digraph(name=f'cluster_{current_cluster_count + 1}')
    cluster_4.attr(sortv=str(sortv_level + 200), packmode=f'array_tu{len(clusters)}', label="")
    
    # Loop through and add course clusters
    for cluster in clusters:
        course_cluster_name = f'cluster_{current_cluster_count + 2}'
        course_cluster = Digraph(name=course_cluster_name)
        # Increment course_counter for the next cluster
        course_counter += 1
        course_sortv = sortv_level + 200 + (course_counter * 10)   
        course_cluster.attr(sortv=str(course_sortv), 
                            packmode='array_tu1', 
                            label="")
                            
        current_cluster_count += 1
              
        # Add course nodes
        node_list = nodes_df[nodes_df['Cluster'] == cluster].iloc[0].tolist()[2:]
        for i, node_name in enumerate(node_list):
            if pd.notna(node_name):
                if i == 0:
                  fill_color = lighten_color(node_color, factor=0.5)   # Original color for the first node
                else:
                  fill_color = lighten_color(node_color, factor=0.9) 
                font_size = '13' if i == 0 else '10'
                # If this is the first node, set the cluster background to a lighter color
                wrapped_node_name = wrap_text(node_name, 20)  # Assuming 20 characters width
                numbered_node_name = f"{level_counter}.{current_cluster_count + 1}.{i + 1}"
                course_cluster.node(numbered_node_name, 
                                  label=wrapped_node_name, 
                                  fillcolor=fill_color,
                                  fontsize=font_size)

        # Append course cluster subgraph to cluster_4
        cluster_4.subgraph(course_cluster)

    # Append the level cluster and course clusters to cluster_2
    cluster_2.subgraph(cluster_level)
    cluster_2.subgraph(cluster_4)

    # Increment current_cluster_count based on the number of clusters created
    current_cluster_count += len(clusters)  # Adding +1 for the level cluster itself
    level_counter += 1  # Increment level counter for the next iteration

# Finally, add cluster_2 to cluster_1, and cluster_1 to the main graph
cluster_1.subgraph(cluster_2)
dot.subgraph(cluster_1)

# Render the graph to a file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'curriculum_viz_pretty_{timestamp}'
dot.render(output_file)

print(f"Graph image saved as {output_file}.png")
