import pytest
from models.tool import ToolModel
from services.tool import Tool
from tests.test_tool_model import get_default_tool
from config.config import Settings

@pytest.fixture
async def tool_fixture() -> tuple[ToolModel, str]:
    default_tool: ToolModel = get_default_tool()
    tool_id: str = Tool.create_in_db(default_tool)
    return default_tool, tool_id

@pytest.mark.asyncio
async def test_get_tool(tool_fixture):
    tool, tool_id = await tool_fixture
    fetched_tool = Tool.get_in_db(tool_id)
    assert fetched_tool['name_for_human'] ==  tool.name_for_human
    Tool.delete_in_db(tool_id)

@pytest.mark.asyncio
async def test_update_tool(tool_fixture):
    tool, tool_id = await tool_fixture
    update = tool.to_dict()
    update['description_for_human'] = 'Updated description'
    updated_tool = Tool.update_in_db(tool_id, update)
    assert updated_tool['description_for_human'] == 'Updated description'
    Tool.delete_in_db(tool_id)

@pytest.mark.asyncio
async def test_delete_tool(tool_fixture):
    _, tool_id = await tool_fixture
    deletion_result = Tool.delete_in_db(tool_id)
    assert deletion_result is True
