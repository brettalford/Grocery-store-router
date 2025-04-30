import tkinter as tk
from tkinter import simpledialog
from main import GraphVisualization


class GraphInputGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.visualization = GraphVisualization()

    def get_input(self):
        # Get user input for number of vertices
        num_vertices = simpledialog.askinteger("Input", "Enter number of vertices:", parent=self.root)
        
        edges = []
        for i in range(num_vertices):
            for j in range(i+1, num_vertices):  # Avoid repeated edges
                weight = simpledialog.askinteger("Input", f"Enter edge weight between Node {i} and Node {j}:", parent=self.root)
                edges.append((i, j, weight))
        
        return num_vertices, edges

    def show_graph(self, num_vertices, edges):
        # Pass the user input to main logic
        self.visualization.construct_graph(num_vertices, edges)
        self.visualization.visualize_graph()

    def show_mst(self, mst_edges):
        # Highlight the MST edges
        self.visualization.highlight_mst(mst_edges)


def run_gui():
    # Initialize the GUI and gather user input
    gui = GraphInputGUI()
    num_vertices, edges = gui.get_input()

    # Show the graph visualization with the user-defined edges
    gui.show_graph(num_vertices, edges)

    # Run MST and show result
    mst_edges = gui.visualization.find_mst()
    gui.show_mst(mst_edges)

    # Optionally, show the Eulerian Circuit
    eulerian_circuit = gui.visualization.find_eulerian_circuit()
    print("\nEulerian Circuit:")
    print(" -> ".join([f"Node {node}" for node in eulerian_circuit]))


if __name__ == "__main__":
    run_gui()
