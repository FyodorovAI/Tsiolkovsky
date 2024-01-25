from fastapi import FastAPI, Depends, HTTPException, Security, Body, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN
import jwt
from typing import List
import uvicorn

from services.tool import Tool
from services.health_check import HealthUpdate
from models.tool import ToolModel
from models.health_check import HealthUpdateModel
from config.supabase import get_supabase
from config.config import Settings

app = FastAPI()
supabase = get_supabase()
settings = Settings()
security = HTTPBearer()

async def authenticate(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        # Perform additional validation checks as needed (e.g., expiration, issuer, audience)
        return payload  # Or a user object based on the payload
    except jwt.PyJWTError as e:
        print(f"JWT error: {str(e)}")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        ) from e


# Tsiolkovsky API
@app.get('/')
def root():
    return 'Tsiolkovsky API v1'

# Tools endpoints
@app.post('/tools')
def create_tool(tool: ToolModel, user = Depends(authenticate)):
    Tool.create_in_db(tool)
    return tool

@app.get('/tools')
def get_tools(user = Depends(authenticate)):
    return Tool.get_all_in_db()

@app.get('/tools/{id}')
def get_tool(id: str, user = Depends(authenticate)):
    return Tool.get_in_db(id)

@app.post('/tools/{id}/health')
def create_health_update(id: str, health_update: HealthUpdateModel, user = Depends(authenticate)):
    return HealthUpdate.save_health_check(health_update)

@app.put('/tools/{id}')
def update_tool(id: str, tool: ToolModel, user = Depends(authenticate)):
    return Tool.update_in_db(id, tool)

@app.delete('/tools/{id}')
def delete_tool(id: str, user = Depends(authenticate)):
    return Tool.delete_in_db(id)

# Health check endpoints
@app.get('/tools/{id}/health')
def get_health_updates(id: str, user = Depends(authenticate)):
    HealthUpdate.get_health_checks(id)

@app.post('/tools/{id}/health')
def create_health_update(id: str, health_update: HealthUpdateModel, user = Depends(authenticate)):
    if id == health_update.tool_id:
        return HealthUpdate.save_health_check(health_update)
    else:
        raise HTTPException(status_code=400, detail="Tool ID does not match health update tool ID")

@app.get('/tools/{id}/health')
def get_health_updates(id: str, user = Depends(authenticate)):
    updates = HealthUpdate.get_health_checks(id)
    if not updates:
        updates = []
    return updates

# User endpoints
@app.post('/users/sign_up')
async def sign_up(email: str = Body(...), password: str = Body(...)):
    try:
        user = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        return {"message": "User created successfully", "jwt": user.session.access_token}
    except Exception as error:
        print(f"Sign up error: {error}")
        raise HTTPException(status_code=400, detail=error)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
