from fastapi import FastAPI, Depends, HTTPException, Security, Body, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import List
import uvicorn

from fyodorov_utils.auth.auth import authenticate
from fyodorov_utils.decorators.logging import error_handler

from services.tool import Tool
from services.health_check import HealthUpdate
from models.tool import ToolModel
from models.health_check import HealthUpdateModel
from services.plugin import Plugin

app = FastAPI(title="Tsiolkovsky", description="A service for managing agent tools", version="0.0.1")


# Tsiolkovsky API
@app.get('/')
@error_handler
def root():
    return 'Tsiolkovsky API v1'

@app.get('/health')
@error_handler
def health_check():
    return 'OK'

# User endpoints
from fyodorov_utils.auth.endpoints import users_app
app.mount('/users', users_app)

# Tools endpoints
@app.get('/.well-known/{name}.json')
@error_handler
def get_plugin_well_known(name: str):
    return Plugin.get_plugin(name)

@app.post('/tools')
@error_handler
def create_tool(tool: ToolModel, user = Depends(authenticate)):
    print(f"User: {user}")
    Tool.create_in_db(tool, user['session_id'])
    return tool

@app.get('/tools')
@error_handler
def get_tools(limit: int = 10, created_at_lt: datetime = datetime.now(), user = Depends(authenticate)):    
    return Tool.get_all_in_db(limit = limit, created_at_lt = created_at_lt)

@app.get('/tools/{id}')
@error_handler
def get_tool(id: str, user = Depends(authenticate)):
    return Tool.get_in_db(id)

@app.put('/tools/{id}')
@error_handler
def update_tool(id: str, tool: ToolModel, user = Depends(authenticate)):
    return Tool.update_in_db(id, tool)

@app.delete('/tools/{id}')
@error_handler
def delete_tool(id: str, user = Depends(authenticate)):
    return Tool.delete_in_db(id)

# Health check endpoints
@app.post('/tools/{id}/health')
@error_handler
def create_health_update(id: str, health_update: HealthUpdateModel, user = Depends(authenticate)):
    if id == health_update.tool_id:
        print(f"Updating tool {id} with health update: {health_update}")
        health = HealthUpdate(
            tool_id = health_update.tool_id,
            health_status = health_update.health_status,
            api_url = health_update.api_url,
        )
        return health.save_health_check()
    else:
        raise HTTPException(status_code=400, detail="Tool ID in URL does not match health update tool ID")

@app.get('/tools/{id}/health')
@error_handler
def get_health_updates(id: str, user = Depends(authenticate)):
    updates = HealthUpdate.get_health_checks(id)
    if not updates:
        updates = []
    return updates


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
