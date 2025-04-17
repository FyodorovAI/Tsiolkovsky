from fastapi import FastAPI, Depends, HTTPException, HTTPException, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Header
from datetime import datetime
import uvicorn
import yaml

from fyodorov_utils.auth.auth import authenticate
from fyodorov_utils.decorators.logging import error_handler

from services.tool_v2 import MCPTool as Tool
from fyodorov_llm_agents.tools.mcp_tool import MCPTool as ToolModel
from api_v1 import api_v1

app = FastAPI(title="Tsiolkovsky", description="A service for managing agent tools", version="0.0.1")
app.mount('/v1', api_v1)

# Tsiolkovsky API
@app.get('/')
@error_handler
def root():
    return 'Tsiolkovsky API v2'

@app.get('/health')
@error_handler
def health_check():
    return 'OK'

# User endpoints
from fyodorov_utils.auth.endpoints import users_app
app.mount('/users', users_app)

# Tools endpoints
@app.get('/.well-known/{user_id}/{name}.yaml')
@error_handler
async def get_plugin_well_known(user_id: str, name: str, authorization: str = Header(None)):
    user = None
    if authorization and authorization.startswith("Bearer "):
        try:
            token = authorization.split(" ")[1]
            creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
            user = await authenticate(creds)
            print(f"User: {user}")
        except Exception as e:
            print("User not found", e)
    if user:
        tool_dict = Tool.get_by_user_and_name_in_db(user['session_id'], user_id, name).to_plugin()
    else:
        tool_dict = Tool.get_by_user_and_name_in_db(None, user_id, name).to_plugin()
    yaml_str = yaml.dump(tool_dict)
    return Response(content=yaml_str, media_type="application/x-yaml")

@app.post('/tools/yaml')
@error_handler
async def create_tool_from_yaml(request: Request, user = Depends(authenticate)):
    try:
        tool_yaml = await request.body()
        tool = ToolModel.from_yaml(tool_yaml)
        Tool.create_in_db(user['session_id'], tool, user['sub'])
        return tool
    except Exception as e:
        print('Error creating tool from yaml', str(e))
        raise HTTPException(status_code=400, detail="Invalid YAML format")

@app.post('/tools')
@error_handler
def create_tool(tool: ToolModel, user = Depends(authenticate)):
    print(f"User: {user}")
    # Pass the authenticated user's ID when creating the tool in the database
    Tool.create_in_db(user['session_id'], tool, user['sub'])
    return tool

@app.get('/tools')
@error_handler
def get_tools(limit: int = 10, created_at_lt: datetime = datetime.now(), user = Depends(authenticate)):    
    return Tool.get_all_in_db(user['session_id'], user['sub'], limit = limit, created_at_lt = created_at_lt)

@app.get('/tools/{id}')
@error_handler
def get_tool(id: str, user = Depends(authenticate)):
    return Tool.get_in_db(user['session_id'], id)

@app.get('/tools/{id}/agents')
@error_handler
def get_tool_agents(id: str, user = Depends(authenticate)):
    return Tool.get_tool_agents(user['session_id'], id)

@app.post('/tools/{id}/agents')
@error_handler
def set_tool_agents(id: str, agent_ids: list[str],user = Depends(authenticate)):
    return Tool.set_tool_agents(user['session_id'], id, agent_ids)

@app.put('/tools/{id}')
@error_handler
def update_tool(id: str, tool: ToolModel, user = Depends(authenticate)):
    return Tool.update_in_db(user['session_id'], id, tool)

@app.delete('/tools/{id}')
@error_handler
def delete_tool(id: str, user = Depends(authenticate)):
    return Tool.delete_in_db(user['session_id'], id)

# Oauth endpoints
@app.post("/oauth/callback/{service_name}")
async def oauth_callback(service_name: str, request: Request):
    # Extract the necessary data from the callback request
    # This part varies greatly between services and needs to be adapted accordingly
    callback_data = await request.json()

    # Validate and process the callback data
    # This is a simplified example; actual implementation will vary
    access_token = callback_data.get("access_token")
    refresh_token = callback_data.get("refresh_token")
    expires_in = callback_data.get("expires_in")
    user_id = callback_data.get("user_id")  # This will depend on the service

    if not access_token:
        raise HTTPException(status_code=400, detail="Access Token missing")

    # Save the credentials to supabase

    # Return a success response
    return JSONResponse(status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
