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
cugw_df = pd.read_excel('Curriculum_Data_RSES_CUGW.xlsx', sheet_name='CUGW Geochem Mjr')
rses_df = pd.read_excel('Curriculum_Data_RSES_CUGW.xlsx', sheet_name='RSES')

# Convert 'Rank' to string to avoid errors with .str accessor
cugw_df['Rank'] = cugw_df['Rank'].astype(str)
rses_df['Rank'] = rses_df['Rank'].astype(str)

# Check contents of the DataFrames
#print("CUGW DataFrame:\n", cugw_df.head())
#print("RSES DataFrame:\n", rses_df.head())

# Group the data by levels in both dataframes
cluster_groups_cugw = {
    "1000 Level": cugw_df[cugw_df['Rank'].str.contains("1000")]['Cluster'].unique(),
    "2000 Level": cugw_df[cugw_df['Rank'].str.contains("2000")]['Cluster'].unique(),
    "3000 Level": cugw_df[cugw_df['Rank'].str.contains("3000")]['Cluster'].unique(),
    "4000 Level": cugw_df[cugw_df['Rank'].str.contains("4000")]['Cluster'].unique(),
}

cluster_groups_rses = {
    "1000 Level": rses_df[rses_df['Rank'].str.contains("1000")]['Cluster'].unique(),
    "2000 Level": rses_df[rses_df['Rank'].str.contains("2000")]['Cluster'].unique(),
    "3000 Level": rses_df[rses_df['Rank'].str.contains("3000")]['Cluster'].unique(),
    "4000 Level": rses_df[rses_df['Rank'].str.contains("4000")]['Cluster'].unique(),
}

# Define color mapping for levels
level_colors = {
    "1000 Level": "yellowgreen",
    "2000 Level": "turquoise",
    "3000 Level": "cyan",
    "4000 Level": "cadetblue",
}
# Step 1: Determine the number of nodes for each level in each group
node_counts_cugw = {level: cugw_df[cugw_df['Rank'].str.contains(level.split()[0])].shape[0] for level in cluster_groups_cugw.keys()}
node_counts_rses = {level: rses_df[rses_df['Rank'].str.contains(level.split()[0])].shape[0] for level in cluster_groups_rses.keys()}
#print("CUGW Rank Values:", cugw_df['Rank'].unique())
#print("RSES Rank Values:", rses_df['Rank'].unique())

# Step 2: Find the maximum number of nodes for each level
max_node_counts = {level: max(node_counts_cugw.get(level, 0), node_counts_rses.get(level, 0)) for level in cluster_groups_cugw.keys()}

# Initialize the main graph
dot = Digraph(comment='Curriculum Visualization')
dot.attr('graph', layout='osage', pad='0.5,0.5', rankdir='TB', sep="2")
dot.attr('node', shape='rect', width='2', height='0.95', fontname='Arial', fontsize='10', style='filled,rounded', penwidth='0.5')
dot.attr('edge', fontname='Arial', fontsize='10', arrowsize='0.5')

def add_empty_nodes(level_name, current_node_count, max_node_count, cluster_graph, group_prefix):
    if current_node_count < max_node_count:
        for i in range(current_node_count, max_node_count):
            empty_node_id = f"{group_prefix}_{level_name}_empty_{i}"
            cluster_graph.node(empty_node_id, label=" ", style="invisible", shape="point")  # Add invisible nodeprint
            (f"Added empty node: {empty_node_id}")
    else:
        print(f"No empty nodes needed for {level_name}: Current Count = {current_node_count}, Max Count = {max_node_count}")

def create_level_and_cluster_subgraph(major_group, df, parent_graph, cluster_groups):
    major_group_cluster = Digraph(name=f'cluster_{major_group}')
    sortv_topvalue = '1100' if major_group == 'CUGW' else '2100'
    major_group_cluster.attr(label=major_group, sortv=sortv_topvalue, packmode='array_tu1')

    level_order = ['1000 Level', '2000 Level', '3000 Level', '4000 Level']
    sortv_values = [1110, 2110, 3110, 4110]
    previous_level_nodes = []

    level_heights = {}
    total_height_for_level = 0

    # Step 2: Use these heights when creating clusters for each level
    for level_index, (level_name, sortv) in enumerate(zip(level_order, sortv_values), start=1):
            clusters = cluster_groups[level_name]
            color = level_colors.get(level_name, 'lightgray')
            level_courses = df[df['Rank'].str.contains(level_name.split()[0])]  # Check for rank by level number
            level_courses = level_courses[level_courses['Cluster'].isin(clusters)]
            current_node_count = level_courses.shape[0]
            for i in level_courses:
              max_node_height_for_level = pd.Series(df[df['Rank'].str.contains(level_name.split()[0])]['Credit'].max() * 0.55)
              total_height_for_level += max_node_height_for_level.sum()
              #print(total_height_for_level)
            level_heights[level_name] = total_height_for_level

            #max_node_height_for_level = df[df['Rank'].str.contains(level_name.split()[0])]['Credit'].max() * 0.35
            #if pd.isna(max_node_height_for_level):  # Check if max_node_height_for_level is nan
              #max_node_height_for_level = 1  # Set a default height (adjust as needed)
            level_heights[level_name] = total_height_for_level
            #print(f"{major_group}_{level_name}")

            if not level_courses.empty:
              cluster_graph = Digraph(name=f'cluster_{level_index}_{major_group.lower()}')
              cluster_graph.attr(label=level_name, size=f"8,{level_heights[level_name]}", sortv=str(sortv), packmode='array_tu2', color=color)
              print(f"Height: {level_heights[level_name]}")

              # Initialize current_level_nodes for this level
              current_level_nodes = []  # Define current_level_nodes here
              df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce')

              for j, row in level_courses.iterrows():
                  course_name = f"{row['Nodes']}, {row['Credit']} CP"
                  node_id = f"{major_group}_{level_name}_{j}"
                  label_wrap = wrap_text (course_name, 20)
                  fill_color = lighten_color(color, 0.2)
                  min_height = 0.55  # Minimum height based on your design
                  max_label_height = 1  # Height adjustment for longer labels
                  dynamic_height = str(max(min_height, row['Credit'] * 0.35, max_label_height))
                  #print(f'{course_name} {dynamic_height}')
                  cluster_graph.node(node_id, label=label_wrap, fillcolor=fill_color, height=dynamic_height)

                  # Calculate level height after node creation
                  node_heights = [float(cluster_graph.body[i].split('height="')[1].split('"')[0]) for i in range(len(cluster_graph.body)) if 'height="' in cluster_graph.body[i]]
                  level_height = max(node_heights) if node_heights else min_height  # Default to min_height if no nodes
                  # Now set the cluster height attribute
                  cluster_graph.attr(label=level_name, height=str(level_height), sortv=str(sortv), packmode='array_tu2', color=color)

                  # Step 3: Add empty nodes to balance the level
                  #add_empty_nodes(level_name, current_node_count, max_node_count, cluster_graph, major_group)

              # Connect nodes from previous level to current level
              if previous_level_nodes:
                            for prev_node in previous_level_nodes:
                              for curr_node in current_level_nodes:
                                  cluster_graph.edge(prev_node, curr_node)

              major_group_cluster.subgraph(cluster_graph)
              previous_level_nodes = current_level_nodes

    parent_graph.subgraph(major_group_cluster)

# Create wrapper and add subgraphs
wrapper_cluster = Digraph(name='cluster_wrapper')
wrapper_cluster.attr(label='Curriculum Visualization', style='dashed', packmode='array_tu2')

for major_group, df, cluster_groups in [("CUGW", cugw_df, cluster_groups_cugw), ("RSES", rses_df, cluster_groups_rses)]:
    create_level_and_cluster_subgraph(major_group, df, wrapper_cluster, cluster_groups)

# Render the final graph
dot.subgraph(wrapper_cluster)

# Render the graph to a file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'curriculum_viz_{timestamp}'
dot.render(output_file, format='pdf')

print(f"Graph saved as {output_file}.pdf")
