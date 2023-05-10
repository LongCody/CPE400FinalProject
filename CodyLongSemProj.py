#Cody Long
#CPE 400
#Project
#05/08/2023

import random
import networkx as nx
import matplotlib.pyplot as plt

# Define a function for Dijkstra's algorithm with node and edge failures
def dijkstra(G, source, failure_probs):
    dist = {}
    prev = {}
    failed_nodes = set()
    failed_edges = set()
    failed_nodes_list = []
    for node in G.nodes():
        dist[node] = float('inf')
        prev[node] = None
    dist[source] = 0
    Q = list(G.nodes())
    while Q:
        u = min(Q, key=dist.get)
        Q.remove(u)
        if dist[u] == float('inf'):
            break
        for v in G.neighbors(u):
            if (u, v) in failed_edges or v in failed_nodes:
                continue
            if random.random() < failure_probs[v]:
                failed_nodes.add(v)
                failed_nodes_list.append(v)
                print(f"Node {v} has failed.")
                continue
            if v in failed_nodes:
                continue
            alt = dist[u] + G[u][v]['weight']
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
        if dist[u] == float('inf'):
            failed_nodes.add(u)
            print(f"Node {u} has failed.")
            failed_nodes_list.append(u)
        else:
            for v in G.neighbors(u):
                if (u, v) in G.edges() and G[u][v]['weight'] < 0:
                    failed_edges.add((u, v))

    return dist, prev, list(failed_nodes_list)

def remove_failed_nodes(graph, failed_nodes):
    # Create a new copy of the graph
    new_graph = graph.copy()
    
    # Remove nodes from the new graph
    new_graph.remove_nodes_from(failed_nodes)
    
    # Remove edges connected to the failed nodes
    edges_to_remove = list(new_graph.edges(nbunch=failed_nodes))
    new_graph.remove_edges_from(edges_to_remove)
    
    return new_graph

def main():
    # Prompt the user for the number of nodes and the probability of failure for each node
    print("Welcome to the network rerouting simulation!")
    num_nodes = int(input("Enter the number of nodes: "))
    failure_probs = []
    for i in range(num_nodes):
        failure_prob = float(input(f"Enter the probability of failure for node {i}: "))
        failure_probs.append(failure_prob)

    # Create an empty graph
    G = nx.Graph()

    # Add nodes to the graph
    for i in range(num_nodes):
        G.add_node(i)

    # Add random edges to the graph with random weights
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if random.random() < 0.5:
                weight = random.randint(1, 10)
                G.add_edge(i, j, weight=weight)

    # Prompt the user for the source node
    source = int(input("Enter the source node: "))

    # Call Dijkstra's algorithm function to get shortest paths
    dist, prev, failed_nodes_list = dijkstra(G, source, failure_probs)

    new_graph = remove_failed_nodes(G, failed_nodes_list)

    dist2, prev2, failed_nodes_list2 = dijkstra(new_graph, source, failure_probs)

    # Print the shortest paths and distances
    for node in new_graph.nodes():
        path = []
        temp = node
        while prev[temp] is not None:
            path.append(temp)
            temp = prev[temp]
        if len(path) > 0:
            path.append(temp)
            path.reverse()
            print(f"Shortest path from node {source} to node {node}: {path}, distance: {dist[node]:.2f}")
        else:
            print(f"No path from node {source} to node {node}")

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()
    plt.savefig("before.png")
    plt.clf()
    print("Figure before deletions saved in 'before.png'")

    #Draw 2nd Graph
    pos1 = nx.spring_layout(new_graph)
    nx.draw(new_graph, pos1, with_labels = True)
    labels = nx.get_edge_attributes(new_graph, 'weight')
    nx.draw_networkx_edge_labels(new_graph, pos1, edge_labels = labels)
    plt.show()
    plt.savefig("after.png")
    print("Figure after deletions saved in 'after.png'")

    return

if __name__ == '__main__': main()