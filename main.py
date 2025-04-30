import networkx as nx
import matplotlib.pyplot as plt
import random


class GraphVisualization:
    def __init__(self):
        self.G = nx.Graph()

    def construct_graph(self, num_vertices, edges):
        # Create the graph from the user input
        for i in range(num_vertices):
            self.G.add_node(f"Node {i}")

        for edge in edges:
            self.G.add_edge(f"Node {edge[0]}", f"Node {edge[1]}", weight=edge[2])

    def visualize_graph(self):
        # Visualization of the graph
        pos = nx.spring_layout(self.G)  # Positioning of nodes
        nx.draw(self.G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()

    def find_mst(self):
        # Applying Prim's Algorithm to find the Minimum Spanning Tree (MST)
        mst_edges = list(nx.minimum_spanning_edges(self.G, data=True))
        return mst_edges

    def highlight_mst(self, mst_edges):
        # Highlight MST edges in the graph visualization
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold')

        # Highlight the MST edges
        edge_colors = ['red' if (u, v) in mst_edges or (v, u) in mst_edges else 'black' for u, v in self.G.edges()]
        nx.draw_networkx_edges(self.G, pos, edge_color=edge_colors, width=2)

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()

    def find_eulerian_circuit(self):
        # Finding an Eulerian Circuit (Hierholzer's Algorithm)
        multigraph_edges = list(self.G.edges())
        adj = {}
        for u, v in multigraph_edges:
            if u not in adj:
                adj[u] = []
            if v not in adj:
                adj[v] = []
            adj[u].append(v)
            adj[v].append(u)

        stack = []
        circuit = []
        start_vertex = list(adj.keys())[0]  # Start at any vertex with an edge
        stack.append(start_vertex)

        while stack:
            vertex = stack[-1]
            if adj[vertex]:
                next_vertex = adj[vertex].pop()
                adj[next_vertex].remove(vertex)
                stack.append(next_vertex)
            else:
                circuit.append(stack.pop())

        return circuit[::-1]  # Reverse the circuit to get the correct order


def main():
    # Example of graph construction and visualization
    visualization = GraphVisualization()

    # User-defined graph from the GUI
    num_vertices = 5  # Example, this will be passed from GUI.py
    edges = [
        (0, 1, 12),
        (0, 2, 7),
        (1, 2, 4),
        (1, 3, 7),
        (2, 3, 9),
    ]  # Example, edges will be passed from GUI.py

    # Construct and visualize graph
    visualization.construct_graph(num_vertices, edges)
    visualization.visualize_graph()

    # Find and highlight MST
    mst_edges = visualization.find_mst()
    visualization.highlight_mst(mst_edges)

    # Find Eulerian Circuit
    eulerian_circuit = visualization.find_eulerian_circuit()
    print("\nEulerian Circuit:")
    print(" -> ".join([f"Node {node}" for node in eulerian_circuit]))


if __name__ == "__main__":
    main()
