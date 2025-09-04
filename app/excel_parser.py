from datetime import datetime, timezone
from pathlib import Path
import uuid
import openpyxl


def get_graph_from_excel(excel_file_name: str) -> dict:
    sheet = openpyxl.load_workbook(excel_file_name, read_only=True).worksheets[0]
    edges = []
    nodes = set()  # повторяющиеся узлы будут игнорированы

    for row in sheet.iter_rows(values_only=True):
        source, target, node = row
        edges.append(
            {
                'source': source,
                'target': target
            }
        ) 
        nodes.add(node)

    filtered_edges = [
        edge for edge in edges
        if edge['source'] in nodes and edge['target'] in nodes
    ]  # отсеивание веток с несуществующими узлами

    return {
        "id": str(uuid.uuid4()),
        "nodes": list(nodes),
        "edges": filtered_edges,
        "upload_time": datetime.now(timezone.utc).isoformat(),
        "filename": Path(excel_file_name).stem,
    }