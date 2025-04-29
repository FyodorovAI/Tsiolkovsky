from datetime import datetime

import uvicorn
import yaml
from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    Response,
)
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

# User endpoints
from fyodorov_utils.auth.endpoints import users_app
from fyodorov_llm_agents.tools.tool import Tool as ToolModel
from fyodorov_utils.auth.auth import authenticate
from fyodorov_utils.decorators.logging import error_handler
from models.health_check import HealthUpdateModel
from services.health_check import HealthUpdate
from services.tool import Tool

api_v1 = FastAPI(
    title="Tsiolkovsky",
    description="A service for managing agent tools",
    version="0.0.1",
)
api_v1.mount("/users", users_app)


# Tsiolkovsky API
@api_v1.get("/")
@error_handler
def root():
    return "Tsiolkovsky API v1"


@api_v1.get("/health")
@error_handler
def health_check():
    return "OK"


# Tools endpoints
@api_v1.get("/.well-known/{user_id}/{name}.json")
@error_handler
async def get_plugin_well_known(
    user_id: str, name: str, authorization: str = Header(None)
):
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
        return Tool.get_by_user_and_name_in_db(
            user["session_id"], user_id, name
        ).to_plugin()
    else:
        return Tool.get_by_user_and_name_in_db(None, user_id, name).to_plugin()


@api_v1.get("/.well-known/{user_id}/{name}.yaml")
@error_handler
async def get_plugin_well_known_yaml(
    user_id: str, name: str, authorization: str = Header(None)
):
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
        tool_dict = Tool.get_by_user_and_name_in_db(
            user["session_id"], user_id, name
        ).to_plugin()
    else:
        tool_dict = Tool.get_by_user_and_name_in_db(None, user_id, name).to_plugin()
    yaml_str = yaml.dump(tool_dict)
    return Response(content=yaml_str, media_type="application/x-yaml")


@api_v1.post("/tools/yaml")
@error_handler
async def create_tool_from_yaml(request: Request, user=Depends(authenticate)):
    try:
        tool_yaml = await request.body()
        tool = ToolModel.from_yaml(tool_yaml)
        Tool.create_in_db(user["session_id"], tool, user["sub"])
        return tool
    except Exception as e:
        print("Error creating tool from yaml", str(e))
        raise HTTPException(status_code=400, detail="Invalid YAML format")


@api_v1.post("/tools")
@error_handler
def create_tool(tool: ToolModel, user=Depends(authenticate)):
    print(f"User: {user}")
    # Include the user's ID when creating the tool in the database
    Tool.create_in_db(user["session_id"], tool, user["sub"])
    return tool


@api_v1.post("/tools/from-plugin")
@error_handler
def create_tool_from_plugin(plugin: dict, user=Depends(authenticate)):
    print(f"Plugin: {plugin}")
    return Tool.create_from_plugin(user["session_id"], plugin["plugin_url"])


@api_v1.get("/tools")
@error_handler
def get_tools(
    limit: int = 10,
    created_at_lt: datetime = datetime.now(),
    user=Depends(authenticate),
):
    return Tool.get_all_in_db(limit=limit, created_at_lt=created_at_lt)


@api_v1.get("/tools/{id}")
@error_handler
def get_tool(id: str, user=Depends(authenticate)):
    return Tool.get_in_db(user["session_id"], id)


@api_v1.put("/tools/{id}")
@error_handler
def update_tool(id: str, tool: ToolModel, user=Depends(authenticate)):
    return Tool.update_in_db(user["session_id"], id, tool)


@api_v1.delete("/tools/{id}")
@error_handler
def delete_tool(id: str, user=Depends(authenticate)):
    return Tool.delete_in_db(user["session_id"], id)


# Health check endpoints
@api_v1.post("/tools/{id}/health")
@error_handler
def create_health_update(
    id: str, health_update: HealthUpdateModel, user=Depends(authenticate)
):
    if id == health_update.tool_id:
        print(f"Updating tool {id} with health update: {health_update}")
        health = HealthUpdate(
            user["session_id"],
            tool_id=health_update.tool_id,
            health_status=health_update.health_status,
            api_url=health_update.api_url,
        )
        return health.save_health_check()
    else:
        raise HTTPException(
            status_code=400,
            detail="Tool ID in URL does not match health update tool ID",
        )


@api_v1.get("/tools/{id}/health")
@error_handler
def get_health_updates(id: str, user=Depends(authenticate)):
    updates = HealthUpdate.get_health_checks(user["session_id"], id)
    if not updates:
        updates = []
    return updates


@api_v1.post("/oauth/callback/{service_name}")
async def oauth_callback(service_name: str, request: Request):
    # Extract the necessary data from the callback request
    # This part varies greatly between services and needs to be adapted accordingly
    callback_data = await request.json()

    # Validate and process the callback data
    # This is a simplified example; actual implementation will vary
    access_token = callback_data.get("access_token")
    # refresh_token = callback_data.get("refresh_token")
    # expires_in = callback_data.get("expires_in")
    # user_id = callback_data.get("user_id")  # This will depend on the service

    if not access_token:
        raise HTTPException(status_code=400, detail="Access Token missing")

    # Save the credentials to supabase

    # Return a success response
    return JSONResponse(status_code=200)


if __name__ == "__main__":
    uvicorn.run(api_v1, host="0.0.0.0", port=3000)
