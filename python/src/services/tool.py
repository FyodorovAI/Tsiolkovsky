from models.tool import ToolModel
from supabase import create_client, Client
from typing import Union
from config.config import Settings
settings = Settings()
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

class Tool():
    @staticmethod    
    async def createInDB(tool: ToolModel) -> str:
        try:
            result = supabase.table('tools').insert(tool.toDict()).execute()
            tool_id = result.data[0]['id']
            print('Created tool', result.data[0])
            return tool_id
        except Exception as e:
            print('Error creating tool', str(e))
            raise e

    @staticmethod
    async def updateInDB(id: str, tool: dict) -> dict:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            result = supabase.table('tools').update(tool).eq('id', id).execute()
            return result.data[0]
        except Exception as e:
            print('An error occurred while updating tool:', id, str(e))
            raise

    @staticmethod
    async def deleteInDB(id: str) -> bool:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            result = supabase.table('tools').delete().eq('id', id).execute()
            return True
        except Exception as e:
            print('Error deleting tool', str(e))
            raise e

    @staticmethod
    async def getInDB(id: str) -> dict:
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
