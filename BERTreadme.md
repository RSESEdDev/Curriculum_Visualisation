Need API Key from Hugging Face https://huggingface.co/settings/tokens

**Important Variables**
|Variable Name 	|Description|
|---|---|
|excel_file| 	Path to the Excel file containing curriculum data.|
|csv_file| 	Path to the CSV file containing geoBERT text data.|
|nodes_df |	Pandas DataFrame storing node information from the Excel file.|
|label_df 	|Pandas DataFrame storing label information from the CSV file.|
|cluster_relationships_df| 	Pandas DataFrame storing cluster relationship information from the Excel file.|
|model_name| 	Name of the pre-trained BERT model ('bert-base-uncased').|
|tokenizer|	BERT tokenizer object for tokenizing text.|
|model| 	BERT model object for generating embeddings.|
|texts |	List of texts (phrases or nodes) for embedding generation.|
|dot| 	Graphviz object for creating graph visualizations.|
|start_node| 	Name of the root node in the graph.|
|clusters |	Unique cluster names from nodes_df.|
|colors |	List of colors for visualizing clusters.|
|cluster_groups| 	List of cluster groupings based on EMSC patterns.|
|label_mapping |	Dictionary mapping cluster labels to category names.|
|intercluster_edges| 	List to store relationships between nodes in different clusters.|
|threshold| 	Similarity threshold for considering relationships.|
|embeddings_2d| 	NumPy array storing the generated BERT embeddings.|
|kmeans |	KMeans object for clustering embeddings.|
|pre_labels |	Cluster labels assigned by KMeans.|
|decoded_labels |	Category names corresponding to cluster labels.|
|similarity_matrix| 	Matrix of cosine similarity scores between embeddings.|
|node_to_category| 	Dictionary mapping nodes to their assigned categories.|
|color_mapping| 	Dictionary mapping categories to colors for visualization.|
|df_relate| 	Pandas DataFrame storing the relationships between nodes.|
|category_df |	Pandas DataFrame storing texts with their categories and labels.|

**Lessor Variables**
|Variable Name 	|Description |
|---|---|
|secret |	Variable to store an API key (not utilized in the current code).|
|exclude_words| 	List of words to exclude during embedding generation.|
|invisible_node| 	Name of an invisible node used for graph layout.|
|previous_invisible_node| 	Reference to the previous invisible node in a cluster.|
|i, j| 	Loop iterators used for various purposes.|
|group| 	Current cluster group being processed.|
|cluster_with_rank |	Combined string of cluster name and rank.|
|cluster, rank| 	Individual cluster name and rank extracted from cluster_with_rank.|
|g, c| 	Temporary variables representing subgraphs in Graphviz.|
|node_list| 	List of nodes within a specific cluster.|
|first_node|	The first node in a cluster, often highlighted.|
|index, row| 	Variables used for iterating through DataFrames.|
|source_cluster, target_cluster| 	Names of source and target clusters in relationships.|
|source_nodes, target_nodes| 	Lists of nodes in source and target clusters.|
|src_node, tgt_node| 	Individual nodes in source and target clusters.|
|src_embedding, tgt_embedding| 	Embeddings for source and target nodes.|
|similarity |	Cosine similarity score between source and target node embeddings.|
|embeddings_file| 	Path to a file for caching embeddings.|
|node_columns| 	List of column names in nodes_df that start with "Nodes".|
|src, tgt, category |	Variables used for iterating through intercluster edges.|
|edge_color| 	Color assigned to an edge based on its category.|
