from pathlib import Path
import uuid
from fastapi import APIRouter, File, HTTPException, UploadFile, Query
from fastapi.responses import HTMLResponse, JSONResponse
from tinydb import Query as TinyDBQuery

from app.db import graphs_table
from app.excel_parser import get_graph_from_excel
from app.graph import build_graph, find_longest_path, get_graph_image


app_router = APIRouter(tags=["Показ картинки"])


@app_router.get('/')
async def get_main_page() -> HTMLResponse:
    with open(Path('app/static/index.html'), encoding='utf-8') as html_file:
        page_html = html_file.read()
    return HTMLResponse(page_html)


@app_router.post('/upload')
async def upload(file: UploadFile = File(...)):
    if file.filename is not None:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(
                status_code=400,
                detail=(
                    f'Given file with unallowed extension.'
                    'Graph loading is allowed from .xlsx file only.'
                )
            )
        try:
            graph_dict = get_graph_from_excel(
                file_obj=file.file,
                filename=file.filename
            )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail=f'Invalid data in Excel file.'
            )
        graphs_table.insert(graph_dict)

        graph = build_graph(graph_dict)
        image_data = get_graph_image(graph)
        return JSONResponse(
            {
                "image": image_data,
                "longest_path": find_longest_path(graph)
            }
        )


@app_router.get('/graphs')
async def get_graphs_list(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    graphs = graphs_table.all()
    sorted_graphs = sorted(graphs, key=lambda g: g['upload_time'], reverse=True)
    return sorted_graphs[offset:limit + offset]


@app_router.get('/graph/{graph_id}')
async def get_graph_by_id(graph_id: str):
    try:
        uuid.UUID(graph_id)
        query = TinyDBQuery()
        graph_data = graphs_table.search(query.id == graph_id)
        if not graph_data:
            raise HTTPException(status_code=404, detail='Graph not found.')
        graph = build_graph(graph_data[0])
        image_data = get_graph_image(graph)
        return {
            "image": image_data,
            "longest_path": find_longest_path(graph)
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f'Invalid UUID format: {graph_id}')
