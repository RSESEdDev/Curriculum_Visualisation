# RSES Curriculum Visualisation Tool

The RSES Curriculum Visualisation Tool provides an easy way to see an entire undergraduate curriculum at once. There are two py files:

 1. RSES_ Curriculum_Viz_Relational.py 
 2. RSES_Curriculum_Viz_Pretty.py

**RSES_ Curriculum_Viz_Relational.py** 
Generate a .png file which can show both relationships between courses (e.g.: prerequisites) in green and between lecture topics (as cluster nodes) in black.

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


