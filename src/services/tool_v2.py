from datetime import datetime
from fyodorov_utils.config.supabase import get_supabase
from fyodorov_llm_agents.tools.mcp_tool import MCPTool as ToolModel

class MCPTool():
    @staticmethod    
    def create_in_db(access_token: str, tool: ToolModel, user_id: str) -> str:
        try:
            supabase = get_supabase(access_token)
            tool_dict = tool.to_dict()
            tool_dict['user_id'] = user_id
            del tool_dict['id']
            del tool_dict['created_at']
            del tool_dict['updated_at']
            print('creating tool in db', tool_dict)
            result = supabase.table('mcp_tools').insert(tool_dict).execute()
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
            result = supabase.table('mcp_tools').update(tool).eq('id', id).execute()
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
            result = supabase.table('mcp_tools').delete().eq('id', id).execute()
            print('Deleted tool', result)
            return True
        except Exception as e:
            print('Error deleting tool', str(e))
            raise e

    @staticmethod
    def get_in_db(access_token: str, id: str) -> ToolModel:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('mcp_tools').select('*').eq('id', id).limit(1).execute()
            tool_dict = result.data[0]
            tool = ToolModel(**tool_dict)
            return tool
        except Exception as e:
            print('Error fetching tool', str(e))
            raise e

    @staticmethod
    def get_by_user_and_name_in_db(access_token: str, user_id: str, name: str) -> ToolModel:
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('mcp_tools').select('*').eq('user_id', user_id).eq('display_name', name).limit(1).execute()
            tool_dict = result.data[0]
            tool = ToolModel(**tool_dict)
            return tool
        except Exception as e:
            print('Error fetching tool', str(e))
            raise e

    @staticmethod
    def get_all_in_db(access_token: str, user_id: str, limit: int = 10, created_at_lt: datetime = datetime.now()) -> [dict]:
        try:
            supabase = get_supabase(access_token)
            print('got supabase for getting tools', supabase)
            print('getting tools from db for user', user_id)
            result = supabase.from_('mcp_tools') \
                .select("*") \
                .limit(limit) \
                .lt('created_at', created_at_lt) \
                .order('created_at', desc=True) \
                .execute()
            print('got tools from db', result)
            tools = result.data
            return tools
        except Exception as e:
            print('Error fetching tools', str(e))
            raise e
