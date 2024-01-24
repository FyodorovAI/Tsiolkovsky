import pytest
from models.tool import ToolModel
from services.tool import Tool
from tests.test_tool_model import get_default_tool
from config.config import Settings

tool_id: str = None
@pytest.fixture
async def tool_fixture() -> tuple[ToolModel, str]:
    default_tool: ToolModel = get_default_tool()
    global tool_id
    if tool_id:
        print('Deleting existing tool')
        await Tool.deleteInDB(tool_id)
    tool_id = await Tool.createInDB(default_tool)
    return default_tool, tool_id

@pytest.mark.asyncio
async def test_get_tool(tool_fixture):
    tool, tool_id = await tool_fixture
    fetched_tool = await Tool.getInDB(tool_id)
    assert fetched_tool['name_for_human'] ==  tool.name_for_human

@pytest.mark.asyncio
async def test_update_tool(tool_fixture):
    tool, tool_id = await tool_fixture
    update = tool.toDict()
    update['description_for_human'] = 'Updated description'
    updated_tool = await Tool.updateInDB(tool_id, update)
    assert updated_tool['description_for_human'] == 'Updated description'

@pytest.mark.asyncio
async def test_delete_tool(tool_fixture):
    _, tool_id = await tool_fixture
    deletion_result = await Tool.deleteInDB(tool_id)
    assert deletion_result is True
