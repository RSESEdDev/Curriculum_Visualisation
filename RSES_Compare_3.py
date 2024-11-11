import pandas as pd
import datetime
from graphviz import Digraph
from matplotlib.colors import to_rgb, to_hex
import matplotlib.colors as mcolors

def lighten_color(color, factor=0.5):
    rgb = mcolors.to_rgba(color)
    lightened_rgb = [min(c + factor * (1 - c), 1.0) for c in rgb[:3]]
    return mcolors.to_hex(lightened_rgb)

def wrap_text(text, max_width):
    text = str(text)  # This line converts any data type to string
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > max_width:
            wrapped_lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line += word + " "

    if current_line:
        wrapped_lines.append(current_line.strip())

    return '\n'.join(wrapped_lines)

# Load data from Excel
first_df = pd.read_excel('HonoursViz.xlsx', sheet_name='first')
second_df = pd.read_excel('HonoursViz.xlsx', sheet_name='second')
#third_df = pd.read_excel('EarthSciMjrlsx', sheet_name='third')

# Convert 'Rank' to string to avoid errors with .str accessor
first_df['Rank'] = first_df['Rank'].astype(str)
second_df['Rank'] = second_df['Rank'].astype(str)
#third_df['Rank'] = third_df['Rank'].astype(str)

# Group the data by levels in both dataframes
cluster_groups_first = {
    "4000 Level": first_df[first_df['Rank'].str.contains("4000")]['Cluster'].unique(),
   # "2000 Level": first_df[first_df['Rank'].str.contains("2000")]['Cluster'].unique(),
   # "3000 Level": first_df[first_df['Rank'].str.contains("3000")]['Cluster'].unique(),
    }

cluster_groups_second = {
    "4000 Level": second_df[second_df['Rank'].str.contains("4000")]['Cluster'].unique(),
   # "2000 Level": second_df[second_df['Rank'].str.contains("2000")]['Cluster'].unique(),
   # "3000 Level": second_df[second_df['Rank'].str.contains("3000")]['Cluster'].unique(),
    }

#cluster_groups_third = {
#    "1000 Level": third_df[third_df['Rank'].str.contains("1000")]['Cluster'].unique(),
#    "2000 Level": third_df[third_df['Rank'].str.contains("2000")]['Cluster'].unique(),
#    "3000 Level": third_df[third_df['Rank'].str.contains("3000")]['Cluster'].unique(),
#    }

# Define color mapping for levels
level_colors = {
    "1000 Level": "yellowgreen",
    "2000 Level": "turquoise",
    "3000 Level": "cyan",
    "4000 Level": "#C3B1E1",
    }
# Step 1: Determine the number of nodes for each level in each group
node_counts_first = {level: first_df[first_df['Rank'].str.contains(level.split()[0])].shape[0] for level in cluster_groups_first.keys()}
node_counts_second = {level: second_df[second_df['Rank'].str.contains(level.split()[0])].shape[0] for level in cluster_groups_second.keys()}
#node_counts_third = {level: third_df[third_df['Rank'].str.contains(level.split()[0])].shape[0] for level in cluster_groups_third.keys()}

# Step 2: Find the maximum number of nodes for each level
max_node_counts = {level: max(node_counts_first.get(level, 0), node_counts_second.get(level, 0)) for level in cluster_groups_first.keys()}
#max_node_counts = {level: max(node_counts_first.get(level, 0), node_counts_second.get(level, 0), node_counts_third.get(level, 0)) for level in cluster_groups_first.keys()}
# Initialize the main graph
dot = Digraph(comment='Climate Science Major')
dot.attr('graph', layout='osage', pad='0.5,0.5', rankdir='LR', sep="2")
dot.attr('node', shape='rect', fixedsize='True', width='1.8', height='0.95', fontname='Arial', fontsize='10', style='filled,rounded', penwidth='0.5')
dot.attr('edge', fontname='Arial', fontsize='10', arrowsize='0.5')

def add_empty_nodes(level_name, current_node_count, max_node_count, cluster_graph, group_prefix):
    if current_node_count < max_node_count:
        print(f"Adding empty nodes for {level_name}: Current Count = {current_node_count}, Max Count = {max_node_count}")
        for i in range(current_node_count, max_node_count):
            empty_node_id = f"{group_prefix}_{level_name}_empty_{i}"
            cluster_graph.node(empty_node_id, label="", style="invisible")  # Add invisible node
            print(f"Added empty node: {empty_node_id}")
    else:
        print(f"No empty nodes needed for {level_name}: Current Count = {current_node_count}, Max Count = {max_node_count}")


# Function to create level and cluster subgraphs
def create_level_and_cluster_subgraph(major_group, df, parent_graph, cluster_groups):  
    major_group_cluster = Digraph(name=f'cluster_{major_group.replace(" ", "_").lower()}')
    sortv_topvalue = '1100' if major_group == 'First Semester' else '2100'
    major_group_cluster.attr(label=major_group, sortv=sortv_topvalue, packmode='array_tu1')

    # Define the order of levels
    level_order = [
                   #'1000 Level', 
                   #'2000 Level', 
                   #'3000 Level', 
                   '4000 Level']
    sortv_values = [
        1110
        #, 
        #2110, 
        #3110, 
        #4110
        ]  # Sort values for each level
    previous_level_nodes = []

    for level_index, (level_name, sortv) in enumerate(zip(level_order, sortv_values), start=1):
        clusters = cluster_groups[level_name]
        color = level_colors.get(level_name, 'lightgray')

        # Filter courses for this level based on the clusters defined
        level_courses = df[df['Rank'].str.contains(level_name.split()[0])]  # Check for rank by level number
        
        # Further filter to ensure they are in the right cluster
        level_courses = level_courses[level_courses['Cluster'].isin(clusters)]
        current_node_count = level_courses.shape[0]
        print(current_node_count)
        max_node_count = max_node_counts.get(level_name, 0)  # Get the max count for this level
        print() 
        # Print to verify the correct courses are retrieved
        #print(f"Processing {level_name} for {major_group}: {level_courses.shape[0]} courses found.")
        #print(level_courses[['Nodes', 'Cluster']])  # Check the relevant columns
        
        cluster_graph = Digraph(name=f'cluster_{level_index}_{major_group.lower()}')
        cluster_graph.attr(label=level_name, sortv=str(sortv), packmode='array_tu2', color=color)
                         
        # Initialize current_level_nodes for this level
        current_level_nodes = []  # Define current_level_nodes here

        for j, row in level_courses.iterrows():
                course_name = row['Nodes']
                node_id = f"{major_group}_{level_name}_{j}"
                label_wrap = wrap_text(course_name, 20)
                fill_color = lighten_color(color, 0.2)
                cluster_graph.node(node_id, label=label_wrap, fillcolor=fill_color)       
                #print(f"Added node: {node_id} with label: {label}")
            
            # Step 3: Add empty nodes to balance the level
        add_empty_nodes(level_name, current_node_count, max_node_count, cluster_graph, major_group)

            # Add edges to connect current level to previous level
        if previous_level_nodes:  # Check if there are nodes from the previous level
                for prev_node in previous_level_nodes:
                    for curr_node in current_level_nodes:
                        cluster_graph.edge(prev_node, curr_node)  # Connect previous level to current level
                        #print(f"Added edge from {prev_node} to {curr_node}")
            
        major_group_cluster.subgraph(cluster_graph)
        previous_level_nodes = current_level_nodes  # Update for the next iteration

    parent_graph.subgraph(major_group_cluster)


# Updated section for creating subgraphs for each major group with sortv adjustments
wrapper_cluster = Digraph(name='cluster_wrapper')
wrapper_cluster.attr(label='Earth Science Honours', style='dashed', rank='same', packmode='array_tu3')

# Define each subgraph's rank explicitly to guide horizontal ordering
first_semester_rank = "0"  # Adjusted values to encourage left-to-right placement
winter_autumn_rank = "1"
#second_semester_rank = "2"

# Adjust the major group creation to explicitly include rankdir setting
for major_group, df, cluster_groups, sortv in [
    ("First Semester", first_df, cluster_groups_first, '1100'),
    ("Second Semester", second_df, cluster_groups_second, '1200'),
 #   ("Second Semester", third_df, cluster_groups_third, '1300')
]:
    major_group_cluster = Digraph(name=f'cluster_{major_group.lower().replace(" ", "_")}')
    major_group_cluster.attr(label=major_group, sortv=sortv, packmode='array_tu1')
    create_level_and_cluster_subgraph(major_group, df, wrapper_cluster, cluster_groups), cluster_groups
dot.subgraph(wrapper_cluster)

# Render the graph to a file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'honours_sci_{timestamp}'
dot.render(output_file, format='png')

print(f"Graph saved as {output_file}.png") 
