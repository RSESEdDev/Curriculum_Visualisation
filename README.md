# RSES Curriculum Visualisation Tool

The RSES Curriculum Visualisation Tool provides an easy way to see an entire undergraduate curriculum at once.  This relies on GraphViz clusters, the code generates a Graph output and there is a handy tool here https://magjac.com/graphviz-visual-editor/ for visualing this and testing changes, as well as either a png or pdf file. There are two py files:

 1. RSES_ Curriculum_Viz_Relational.py 
 2. RSES_Curriculum_Viz_Pretty.py

**RSES_ Curriculum_Viz_Relational.py** 
Generates a .png file which can show both relationships between courses (e.g.: prerequisites) in green and between lecture topics (as cluster nodes) in black.

**RSES_Curriculum_Viz_Pretty.py**
Generates a .PDF file showing all program units and lecture topics in a structured and hierarchical format.  This file may be useful for printing as a poster.   

# How to use

Populate Curriculum_Data_Blank.xlsx as follows:
NB: All node columns must be populated with unique entries!

1. Sheet 'Nodes' - enter the program_code into the Start column, unit codes into the Cluster column and lecture or titles as appropriate in columns Nodes1 - 24.  Being designed for HE undergraduate programs, Lectures 1 - 24 are assumed.  You can add more columns are required just ensure they are named 'Node*x*' as required.  In the Rank column rank the units 1-> as appropriate for level groupings.  For this purpose a level would be 1000 level courses, 2000 level courses and so on.

*If you want to display relationships:*

 1. Cluster Relationships' sheet will provide the data to show relationships between courses (e.g.: prerequisites), these will show as green arrows.  Enter in the first course under SourceCluster column and the in the TargetCluster enter the course that the first course is a per-requiste for.
 2. 'Relationships' sheet will provide the data to show relationships between lectures (nodes) as black arrows.  Enter the earliest lecture in the Source column (exactly as listed in the Nodes sheet) and the later lecture in the Target column.

Note displaying relationships gets messy fast - this is recommended only for streams or a series of related courses.

To summarise, depending on what vis you want you will need to fill in the following sheets:

|                |Pretty                       |Relational                         |
|----------------|-------------------------------|-----------------------------|
|Node|Yes          |Yes           |
|Cluster Relationships         |No           |Yes           |
|Relationships         |No|Yes|

# For Pretty & Relational
Update the path and file name as required:

    nodes_df = pd.read_excel('Curriculum_Data_Blank.xlsx', sheet_name='Nodes')

# For Pretty - Find nodes
Update: 'unitname_1', 'unitname_2' & 'unitname_2' to match the pattern of your entry in the Cluster column (minus any unique identifier past the unit level eg: unitname_1 not unitname_1001) as per below.

    cluster_groups = {
    "1000 Level": nodes_df[nodes_df['Cluster'].str.contains('unitname_1')]['Cluster'].unique(),
    "2000 Level": nodes_df[nodes_df['Cluster'].str.contains('unitname_2')]['Cluster'].unique(),
    "3000 Level": nodes_df[nodes_df['Cluster'].str.contains('unitname_3')]['Cluster'].unique(),
    }

# For Pretty - Change colours
To change colours for each level update as per below. No need to use RGB or Hex, the program will convert if necessary and also do the colour fades for the the nodes and headings.

    level_colors = {
    "1000 Level": ("yellowgreen", "yellowgreen"), # Cluster color, first node color
    "2000 Level": ("turquoise", "turquoise"), # Cluster color, first node color
    "3000 Level": ("lightskyblue", "lightskyblue"), # Cluster color, first node color
    }

# For Relational - Find nodes
Update: 'unitname_1', 'unitname_2' & 'unitname_3' to match the pattern of your entry in the Cluster column as per below.

    cluster_groups = [
    [f"{cluster}_{nodes_df[nodes_df['Cluster'] == cluster]['Rank'].iloc[0]}"
     for cluster in nodes_df['Cluster'].unique() if cluster.startswith('unitname_1')],
    [f"{cluster}_{nodes_df[nodes_df['Cluster'] == cluster]['Rank'].iloc[0]}"
     for cluster in nodes_df['Cluster'].unique() if cluster.startswith('unitname_2')],
    [f"{cluster}_{nodes_df[nodes_df['Cluster'] == cluster]['Rank'].iloc[0]}"
     for cluster in nodes_df['Cluster'].unique() if cluster.startswith('unitname_3')],
    # ... add more groups as needed  ]





