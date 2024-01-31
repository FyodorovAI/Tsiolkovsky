from fastapi import FastAPI, Depends, HTTPException, Security, Body, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN
from datetime import datetime, timedelta
import jwt
from typing import List
import uvicorn

import sys
sys.path.append('/path/to/venv/lib/python3.11/site-packages')
import fyodorov_utils


import sys
print("System executable: ", sys.executable)

from fyodorov_utils.auth.auth import authenticate
from fyodorov_utils.decorators.logging import error_handler

from services.tool import Tool
from services.health_check import HealthUpdate
from models.tool import ToolModel
from models.health_check import HealthUpdateModel
from config.supabase import get_supabase
from config.config import Settings

app = FastAPI()
supabase = get_supabase()


# Tsiolkovsky API
@app.get('/')
@error_handler
def root():
    return 'Tsiolkovsky API v1'

# User endpoints
from fyodorov_utils.auth.endpoints import users_app
app.mount('/users', users_app)

@app.get('/health')
@error_handler
def health_check():
    return 'OK'

@app.get('/.well-known/{name}.json')
@error_handler
def get_plugin_well_known(name: str):
    plugin = Plugin.get_plugin(name)
    return plugin

# Tools endpoints
@app.post('/tools')
@error_handler
def create_tool(tool: ToolModel, user = Depends(authenticate)):
    Tool.create_in_db(tool)
    return tool

@app.get('/tools')
@error_handler
def get_tools(user = Depends(authenticate), limit: int = 10, created_at_lt: datetime = datetime.now()):    
    return Tool.get_all_in_db(limit = limit, created_at_lt = created_at_lt)

@app.get('/tools/{id}')
@error_handler
def get_tool(id: str, user = Depends(authenticate)):
    return Tool.get_in_db(id)

@app.post('/tools/{id}/health')
@error_handler
def create_health_update(id: str, health_update: HealthUpdateModel, user = Depends(authenticate)):
    return HealthUpdate.save_health_check(health_update)

@app.put('/tools/{id}')
@error_handler
def update_tool(id: str, tool: ToolModel, user = Depends(authenticate)):
    return Tool.update_in_db(id, tool)

@app.delete('/tools/{id}')
@error_handler
def delete_tool(id: str, user = Depends(authenticate)):
    return Tool.delete_in_db(id)

# Health check endpoints
@app.get('/tools/{id}/health')
@error_handler
def get_health_updates(id: str, user = Depends(authenticate)):
    HealthUpdate.get_health_checks(id)

@app.post('/tools/{id}/health')
@error_handler
def create_health_update(id: str, health_update: HealthUpdateModel, user = Depends(authenticate)):
    if id == health_update.tool_id:
        return HealthUpdate.save_health_check(health_update)
    else:
        raise HTTPException(status_code=400, detail="Tool ID does not match health update tool ID")

@app.get('/tools/{id}/health')
@error_handler
def get_health_updates(id: str, user = Depends(authenticate)):
    updates = HealthUpdate.get_health_checks(id)
    if not updates:
        updates = []
    return updates


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
