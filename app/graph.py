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


def write_graph_in_bytes(graph) -> BytesIO:
    buffer = BytesIO()
    plt.figure(figsize=(5, 3), dpi=60)
    pos = nx.spring_layout(graph, k=1, iterations=50)

    nx.draw_networkx_nodes(
        graph, pos, 
        node_size=800, 
        node_color='lightblue',
        edgecolors='black',
        linewidths=0.5
    )
    nx.draw_networkx_edges(
        graph, pos, 
        edge_color='black',
        width=0.5
    )
    nx.draw_networkx_labels(
        graph, pos, 
        font_size=12, 
    )  
    plt.axis('off')
    plt.tight_layout(pad=0.1) 
    plt.margins(0.1)
    plt.savefig(buffer, format='png', dpi=150)
    plt.close()

    buffer.seek(0)
    return buffer


def get_graph_image(graph: nx.Graph) -> str:
    buffer = write_graph_in_bytes(graph)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"
