
from pydantic import BaseModel
import re
from models.health_check import HealthUpdateModel
from supabase import  Client
from config.supabase import get_supabase

supabase: Client = get_supabase()

class HealthUpdate(BaseModel):
    health_update: HealthUpdateModel

    async def update_tool_in_db(self) -> dict:
        update = { 'health_status': self.health_update.health_status }
        if self.health_update.api_url:
            update['api_url'] = str(self.health_update.api_url)
        try:
            result = supabase.table('tools').update(update).eq('id', self.health_update.tool_id).execute()
            update = result.data[0]
            print('Updated tool with new API URL', update)
            return update
        except Exception as e:
            print(f"Error updating tool with id {self.health_update.tool_id} "
                  f"and health status {self.health_update.health_status} "
                  f"with API URL {self.health_update.api_url}: {str(e)}")
            raise e

    async def save_health_check_in_db(self) -> dict:
        try:
            result = supabase.table('tools_health_checks').insert(self.health_update.to_dict()).execute()
            update = result.data[0]
            print('Saved health update', update)
            return update
        except Exception as e:
            print('Error saving health update', str(e))
            raise e

    async def save_health_check(self):
        await self.update_tool_in_db()
        await self.save_health_check_in_db()

    @staticmethod
    async def get_health_checks(tool_id: str) -> [dict]:
        try:
            result = supabase.table('tools_health_checks') \
                        .select('*') \
                        .eq('tool_id', tool_id) \
                        .order('created_at', desc=True) \
                        .execute()
            data = result.data
            print('Fetched health checks for tool', tool_id, data)
            return data
        except Exception as e:
            print('Error fetching health checks for tool', tool_id, str(e))
            raise e
