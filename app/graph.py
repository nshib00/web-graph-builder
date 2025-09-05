import base64
from io import BytesIO
import networkx as nx
import matplotlib

matplotlib.use('Agg')  # бэкенд matplotlib без GUI, используется для ускорения отрисовки

import matplotlib.pyplot as plt


def build_graph(graph_data: dict) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(graph_data['nodes'])
    edges = (tuple(edge.values()) for edge in graph_data['edges'])
    graph.add_edges_from(edges)
    return graph


def write_graph_in_bytes(graph: nx.Graph, longest_path: list[int]) -> BytesIO:
    buffer = BytesIO()
    plt.figure(figsize=(5, 3), dpi=60)
    pos = nx.spring_layout(graph, k=1, iterations=50)

    nx.draw_networkx_nodes(
        graph, pos, 
        node_size=800, 
        node_color='lightblue',
        edgecolors='black',
        linewidths=0.3
    )
    nx.draw_networkx_edges(
        graph, pos, 
        edge_color='black',
        width=0.3
    )
    nx.draw_networkx_labels(
        graph, pos, 
        font_size=12, 
    )

    if longest_path:
        nx.draw_networkx_nodes(
            graph, pos,
            nodelist=longest_path,
            node_size=800,
            node_color='orange',
            edgecolors='darkorange',
            linewidths=1
        )
    path_edges = []
    for i in range(len(longest_path) - 1):
        path_edges.append((longest_path[i], longest_path[i + 1]))
    nx.draw_networkx_edges(
        graph, pos,
        edgelist=path_edges, 
        edge_color='darkorange',
        width=1
    )  

    plt.axis('off')
    plt.tight_layout(pad=0.1) 
    plt.margins(0.1)
    plt.savefig(buffer, format='png', dpi=150)
    plt.close()

    buffer.seek(0)
    return buffer


def get_graph_image(graph: nx.Graph) -> str:
    buffer = write_graph_in_bytes(
        graph=graph,
        longest_path=find_longest_path(graph)
    )
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"


def dfs_find_longest_path(
    graph: nx.Graph,
    start_node: int,
    visited: set, 
    current_path: list,
    longest_path: list
) -> None:
    visited.add(start_node)
    current_path.append(start_node)

    if len(current_path) > len(longest_path):
        longest_path.clear()
        longest_path.extend(current_path)
    
    # непосещенные соседи стартовой вершины
    neighbors = [n for n in graph.neighbors(start_node) if n not in visited]
    
    # отсекаем ветви, которые не могут превзойти текущий максимум
    for neighbor in neighbors:
        remaining_nodes = len(graph.nodes) - len(visited)
        if len(current_path) + remaining_nodes <= len(longest_path):
            continue  # не можем найти путь длиннее текущего максимума
            
        dfs_find_longest_path(graph, neighbor, visited, current_path, longest_path)
    
    visited.remove(start_node)
    current_path.pop()


def find_longest_path(graph: nx.Graph) -> list[int]:
    if not graph.nodes:
        return []
    if len(graph.nodes) == 1:
        return [next(iter(graph.nodes))]
    
    longest_path = []
    start_nodes = list(graph.nodes())

    max_start_nodes = min(10, len(start_nodes))
    for start_node in start_nodes[:max_start_nodes]:
        if len(longest_path) == len(graph.nodes):
            break
            
        visited = set()
        current_path = []
        dfs_find_longest_path(graph, start_node, visited, current_path, longest_path)
    
    return longest_path
