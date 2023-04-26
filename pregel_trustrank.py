"""
Implementation of Trustrank using pregel framework
"""
import csv
from pregel import Vertex, Pregel

num_workers = 4                                 # No of threads to assign vertices

""" Vertex class for TrustRank algorithm
    Can add instance varibles and methods according to algorithm
"""
class TrustRankVertex(Vertex):
    def __init__(self,id,value,out_vertices,dampingFactor=0.85,iterations=100):
        Vertex.__init__(self,id,value,out_vertices)
        self.dampingFactor = dampingFactor
        self.num_supersteps = iterations

    def update(self):
        # Updating vertex in each superstep
        if self.superstep < self.num_supersteps:
            messages_sum = 0
            for (vertex,message) in self.incoming_messages:
                messages_sum = messages_sum+message
            if self.id not in bad_nodes:
                self.value = self.dampingFactor*messages_sum
            else:
                self.value = self.dampingFactor*messages_sum+(1-self.dampingFactor)/len(bad_nodes)

            # Sending outgoing messages now
            outgoing_message = self.value / len(self.out_vertices)
            self.outgoing_messages = [(vertex_from_id[id],outgoing_message) for (id,weight) in self.out_vertices]
        else:
            self.active = False

""" Compute Pagerank using pregel by assing set of vertices to thread """
def pregelTrustRank(vertices):
    p = Pregel(vertices,num_workers)
    p.run()
    return ([(vertex.id,vertex.value) for vertex in p.vertices])


""" This Function gives initializes trustscores of all nodes """
def initializeTrustScore(nodes,bad_nodes):
    initialTrustScore = []
    for node in nodes:
        if node in bad_nodes:
            initialTrustScore.append(1/len(bad_nodes))
        else:
            initialTrustScore.append(0)
    return initialTrustScore

# Opening Iron_dealers_data.csv
dealers_csv = csv.reader(open('Iron_dealers_data.csv',newline=''))

# Skipping the header
next(dealers_csv)

# Making a list of IDs of dealers(nodes) and deals between them (edges)
nodes = []
edges = {} #This will be a dictionary with key as (Seller ID,Buyer ID)

for row in dealers_csv:
    # Each row has Seller ID, Buyer ID and transaction value 
    sellerID,buyerID,value = int(row[0]),int(row[1]),float(row[2])
    nodes += [sellerID,buyerID]
    # We don't want multiple edges between two same dealers
    key = (sellerID,buyerID)
    if key in edges:
        edges[key]+=value
    else:
        edges[key]=value

nodes = list(set(nodes)) # dealers need to be set of unique IDs
out_edges = {} # Making a dictionary which gives a list of out vertices and corresponding edge weights for given nodeId

# Initializing the out_vertices list for each node
for key,value in edges.items():
    out_edges[key[0]] = []
# Appending the out_vertices list for each node
for key,value in edges.items():
    out_edges[key[0]].append((key[1],value))

# Opening bad.csv
bad_dealers_csv = csv.reader(open('bad.csv',newline=''))

# Skipping the header
next(bad_dealers_csv)

# Making a list of all bad dealers
bad_nodes = []

for row in bad_dealers_csv:
    bad_dealer = int(row[0])
    bad_nodes.append(bad_dealer)

num_vertices = len(nodes)
initial_trust_score = initializeTrustScore(nodes,bad_nodes)

# Initializing List of vertices with modified TrustRankVertex class
vertices = []
# Adding vertices
for i in range(num_vertices):
    if nodes[i] in out_edges:
        vertices.append(TrustRankVertex(nodes[i],initial_trust_score[i],out_edges[nodes[i]]))
    else:
        # If a vertex has no outgoing edge we will link it to every bad node with equal weight
        edges_to_bad_nodes = [(bad_node,1000) for bad_node in bad_nodes]
        vertices.append(TrustRankVertex(nodes[i],initial_trust_score[i],edges_to_bad_nodes))

# Making a dictionary which maps id to vertex object
vertex_from_id = {}
for vertex in vertices:
    vertex_from_id[vertex.id] = vertex

# Getting Final trust scores
nodes_trust_scores = pregelTrustRank(vertices)

nodes_trust_scores = sorted(nodes_trust_scores, key=lambda x: x[1])

for i in range(num_vertices):
    print(f'Scores: {nodes_trust_scores[i]}')