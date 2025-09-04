from pathlib import Path
import uuid
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from tinydb import Query

from app.db import graphs_table
from app.excel_parser import get_graph_from_excel
from app.graph import build_graph, get_graph_image


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
        graph_dict = get_graph_from_excel(file.filename)
        graphs_table.insert(graph_dict)
        # image_data = get_graph_image(build_graph(graph_dict))
    return RedirectResponse("/", status_code=303)


@app_router.get('/graphs')
async def get_graphs_list():
    graphs = graphs_table.all()
    return sorted(graphs, key=lambda g: g['upload_time'], reverse=True)


@app_router.get('/graph/{graph_id}')
async def get_graph_by_id(graph_id: str):
    try:
        uuid.UUID(graph_id)
        query = Query()
        graph_data = graphs_table.search(query.id == graph_id)
        if not graph_data:
            raise HTTPException(status_code=404, detail='Graph not found.')
        graph = build_graph(graph_data[0])
        image_data = get_graph_image(graph)
        return {"image": image_data}
    except ValueError:
        raise HTTPException(status_code=400, detail=f'Invalid UUID format: {graph_id}')
