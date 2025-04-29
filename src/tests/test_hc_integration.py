import pytest
from fyodorov_utils.config.config import Settings
from models.health_check import HealthStatusTypes, HealthUpdateModel
from models.tool import ToolModel
from services.health_check import HealthUpdate
from services.tool import Tool

from tests.test_hc_model import get_default_hc
from tests.test_tool_model import get_default_tool


@pytest.fixture
async def hc_fixture() -> HealthUpdate:
    default_hc: HealthUpdateModel = get_default_hc()
    tool: ToolModel = get_default_tool()
    tool_id: str = Tool.create_in_db(tool)
    default_hc.tool_id = tool_id
    hc = HealthUpdate(health_update=default_hc)
    return hc


@pytest.mark.asyncio
async def test_get_hcs(hc_fixture):
    hc = await hc_fixture
    fetched_hcs = await HealthUpdate.get_health_checks(hc.health_update.tool_id)
    for hc in fetched_hcs:
        assert hc["tool_id"] == hc.health_update.tool_id and HealthStatusTypes(
            hc["health_status"]
        )
    Tool.delete_in_db(hc.health_update.tool_id)


@pytest.mark.asyncio
async def test_update_tool(hc_fixture):
    hc = await hc_fixture
    hc.health_update.health_status = "unhealthy"
    updated_tool = await hc.update_tool_in_db()
    assert updated_tool["health_status"] == "unhealthy"
    Tool.delete_in_db(hc.health_update.tool_id)


@pytest.mark.asyncio
async def test_save_health_check(hc_fixture):
    hc = await hc_fixture
    await hc.save_health_check_in_db()
    Tool.delete_in_db(hc.health_update.tool_id)
