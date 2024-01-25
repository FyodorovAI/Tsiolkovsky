from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from services.tool import Tool
from services.health_check import HealthUpdate
from models.tool import ToolModel
from models.health_check import HealthUpdateModel

app = FastAPI()

@app.get('/')
def root():
    return 'Tsiolkovsky API'

@app.post('/tools')
def create_tool(tool: ToolModel):
    Tool.create_in_db(tool)
    return tool

@app.get('/tools')
def get_tools():
    return Tool.get_all_in_db()

@app.get('/tools/{id}')
def get_tool(id: str):
    return Tool.get_in_db(id)

@app.post('/tools/{id}/health')
def create_health_update(id: str, health_update: HealthUpdateModel):
    return HealthUpdate.save_health_check(health_update)

@app.put('/tools/{id}')
def update_tool(id: str, tool: ToolModel):
    return Tool.update_in_db(id, tool)

@app.delete('/tools/{id}')
def delete_tool(id: str):
    return Tool.delete_in_db(id)

@app.get('/tools/{id}/health')
def get_health_updates(id: str):
    HealthUpdate.get_health_checks(id)

@app.post('/tools/{id}/health')
def create_health_update(id: str, health_update: HealthUpdateModel):
    if id == health_update.tool_id:
        return HealthUpdate.save_health_check(health_update)
    else:
        raise HTTPException(status_code=400, detail="Tool ID does not match health update tool ID")

@app.get('/tools/{id}/health')
def get_health_updates(id: str):
    updates = HealthUpdate.get_health_checks(id)
    if not updates:
        updates = []
    return updates

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
