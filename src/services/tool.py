from models.tool import ToolModel
from typing import Union
from datetime import datetime, timedelta
from supabase import  Client
from config.supabase import get_supabase

supabase: Client = get_supabase()

class Tool():
    @staticmethod    
    def create_in_db(tool: ToolModel) -> str:
        try:
            result = supabase.table('tools').insert(tool.to_dict()).execute()
            tool_id = result.data[0]['id']
            print('Created tool', result.data[0])
            return tool_id
        except Exception as e:
            print('Error creating tool', str(e))
            raise e

    @staticmethod
    def update_in_db(id: str, tool: dict) -> dict:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            result = supabase.table('tools').update(tool).eq('id', id).execute()
            return result.data[0]
        except Exception as e:
            print('An error occurred while updating tool:', id, str(e))
            raise

    @staticmethod
    def delete_in_db(id: str) -> bool:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            result = supabase.table('tools').delete().eq('id', id).execute()
            return True
        except Exception as e:
            print('Error deleting tool', str(e))
            raise e

    @staticmethod
    def get_in_db(id: str) -> dict:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            result = supabase.table('tools').select('*').eq('id', id).limit(1).execute()
            tool = result.data[0]
            print('Fetched tool', tool)
            return tool
        except Exception as e:
            print('Error fetching tool', str(e))
            raise e

    @staticmethod
    def get_all_in_db(limit: int = 10, created_at_lt: datetime = datetime.now()) -> [dict]:
        try:
            result = supabase.table('tools').select('*').limit(limit).lt('created_at', created_at_lt).execute()
            tools = result.data
            print('Fetched tools', tools)
            return tools
        except Exception as e:
            print('Error fetching tools', str(e))
            raise e