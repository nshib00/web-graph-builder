from datetime import datetime, timezone
from pathlib import Path
import uuid
import openpyxl


def to_int_or_none(value):
    try:
        value = int(value)
        if value > 0:
            return value
    except (TypeError, ValueError):
        return None


def get_graph_from_excel(file_obj, filename: str) -> dict:
    workbook = openpyxl.load_workbook(file_obj, data_only=True, read_only=True)
    sheet = workbook.worksheets[0]
    edges = []  
    nodes = set()  # повторяющиеся узлы будут игнорированы

    first_row = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True))
    has_headers = any(
        not isinstance(cell, (int, float)) 
        for cell in first_row
    )  # если хотя бы один элемент первой строки не число - считаем ее заголовком
    start_row = 2 if has_headers else 1

    for row in sheet.iter_rows(min_row=start_row, values_only=True):
        source, target, node = map(to_int_or_none, row)

        if node is not None:
            nodes.add(node)
        if source is not None and target is not None:
            edges.append({"source": source, "target": target})

    filtered_edges = [
        e for e in edges
        if e["source"] in nodes and e["target"] in nodes
    ]

    return {
        "id": str(uuid.uuid4()),
        "nodes": list(nodes),
        "edges": filtered_edges,
        "upload_time": datetime.now(timezone.utc).isoformat(),
        "filename": Path(filename).stem or "<Без названия>",
    }
