from models.tool import ToolModel
from typing import Union
from datetime import datetime, timedelta
from fyodorov_utils.config.supabase import get_supabase

class Tool():
    @staticmethod    
    def create_in_db(access_token: str, tool: ToolModel) -> str:
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('tools').insert(tool.to_dict()).execute()
            tool_id = result.data[0]['id']
            return tool_id
        except Exception as e:
            print('Error creating tool', str(e))
            raise e

    @staticmethod
    def update_in_db(access_token: str, id: str, tool: dict) -> dict:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('tools').update(tool).eq('id', id).execute()
            return result.data[0]
        except Exception as e:
            print('An error occurred while updating tool:', id, str(e))
            raise

    @staticmethod
    def delete_in_db(access_token: str, id: str) -> bool:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('tools').delete().eq('id', id).execute()
            return True
        except Exception as e:
            print('Error deleting tool', str(e))
            raise e

    @staticmethod
    def get_in_db(access_token: str, id: str) -> dict:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('tools').select('*').eq('id', id).limit(1).execute()
            tool = result.data[0]
            return tool
        except Exception as e:
            print('Error fetching tool', str(e))
            raise e

    @staticmethod
    def get_all_in_db(access_token: str, limit: int = 10, created_at_lt: datetime = datetime.now()) -> [dict]:
        try:
            supabase = get_supabase(access_token)
            result = supabase.from_('tools') \
                .select("*") \
                .limit(limit) \
                .lt('created_at', created_at_lt) \
                .order('created_at', desc=True) \
                .execute()
            tools = result.data
            return tools
        except Exception as e:
            print('Error fetching tools', str(e))
            raise e