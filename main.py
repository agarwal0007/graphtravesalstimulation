import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.title("Pathfinding Visualizer")
root.geometry("800x600")

G = nx.Graph()

figure, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(figure, root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def draw_graph():
    ax.clear()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500)
    for node, (x, y) in pos.items():
        cost = 0
        for _, _, edge_data in G.edges(node, data=True):
            cost += edge_data.get('weight', 0)
        ax.text(x, y+0.1, s=f"Cost: {cost}", bbox=dict(facecolor='white', alpha=0.5), horizontalalignment='center')
    canvas.draw_idle()

def add_node():
    node = simpledialog.askstring("Node", "Enter node name")
    if node:
        G.add_node(node)
        draw_graph()

def add_edge():
    node1 = simpledialog.askstring("Edge", "Enter from node")
    node2 = simpledialog.askstring("Edge", "Enter to node")
    cost = simpledialog.askstring("Cost", "Enter edge cost")
    if node1 and node2 and cost:
        try:
            cost_value = float(cost)
            G.add_edge(node1, node2, weight=cost_value)
            draw_graph()
        except ValueError:
            messagebox.showerror("Error", "Invalid cost value")

def heuristic(a, b):
    return 0

def find_all_paths():
    start_node = simpledialog.askstring("Path", "Enter start node")
    algorithm = algorithm_choice.get()
    if start_node:
        try:
            if algorithm == 'Dijkstra':
                paths = {node: nx.dijkstra_path(G, start_node, node) for node in G if node != start_node}
            elif algorithm == 'A*':
                paths = {node: nx.astar_path(G, start_node, node, heuristic=heuristic) for node in G if node != start_node}
            elif algorithm == 'Floyd-Warshall':
                fw_paths = nx.floyd_warshall_predecessor_and_distance(G)
                paths = {node: nx.reconstruct_path(start_node, node, fw_paths[0]) for node in G if node != start_node}
            elif algorithm == 'Bellman-Ford':
                paths = {node: nx.bellman_ford_path(G, start_node, node) for node in G if node != start_node}
            elif algorithm == 'Bidirectional Dijkstra':
                paths = {node: nx.bidirectional_dijkstra(G, start_node, node)[1] for node in G if node != start_node}
            else:
                raise ValueError("Invalid algorithm")
            paths_costs = {end: sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)) for end, path in paths.items()}
            paths_info = "\n".join([f"{start_node} -> {end}: {' -> '.join(path)}, Cost: {cost}" for end, path, cost in zip(paths.keys(), paths.values(), paths_costs.values())])
            messagebox.showinfo(f"Paths and Costs from {start_node} using {algorithm}", paths_info)
        except (nx.NetworkXNoPath, nx.NodeNotFound, ValueError, IndexError) as e:
            messagebox.showerror("Error", str(e))

add_node_button = tk.Button(root, text="Add Node", command=add_node)
add_node_button.pack(side=tk.LEFT)

add_edge_button = tk.Button(root, text="Add Edge", command=add_edge)
add_edge_button.pack(side=tk.LEFT)

algorithm_choice = tk.StringVar()
algorithm_choice.set("Dijkstra")
algorithm_menu = ttk.Combobox(root, textvariable=algorithm_choice, state='readonly')
algorithm_menu['values'] = ('Dijkstra', 'A*', 'Floyd-Warshall', 'Bellman-Ford', 'Bidirectional Dijkstra')
algorithm_menu.pack(side=tk.LEFT)

find_paths_button = tk.Button(root, text="Find All Paths", command=find_all_paths)
find_paths_button.pack(side=tk.LEFT)

draw_graph()
root.mainloop()
