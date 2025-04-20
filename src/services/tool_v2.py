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
    def update_in_db(access_token: str, id: str, tool: ToolModel) -> dict:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            tool_dict = tool.to_dict()
            print('updating tool in db', tool_dict)
            result = supabase.table('mcp_tools').update(tool_dict).eq('id', id).execute()
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
            result = supabase.table('mcp_tools').select('*').eq('user_id', user_id).eq('name', name).limit(1).execute()
            tool_dict = result.data[0]
            tool = ToolModel(**tool_dict)
            return tool
        except Exception as e:
            print('Error fetching tool', str(e))
            raise e

    @staticmethod
    def get_all_in_db(access_token: str, user_id: str = None, limit: int = 10, created_at_lt: datetime = datetime.now()) -> list[dict]:
        try:
            supabase = get_supabase(access_token)
            print('getting tools from db for user', user_id)
            tools = []
            result = supabase.from_('mcp_tools') \
                .select("*") \
                .limit(limit) \
                .lt('created_at', created_at_lt) \
                .order('created_at', desc=True) \
                .execute()
            for tool in result.data:
                tool["id"] = str(tool["id"])
                tool["user_id"] = str(tool["user_id"])
                tool["created_at"] = str(tool["created_at"])
                tool["updated_at"] = str(tool["updated_at"])
                if tool and (tool['public'] == True or (user_id and 'user_id' in tool and tool['user_id'] == user_id)):
                    print('tool is public or belongs to user', tool)
                    tools.append(tool)
            print('got tools from db', len(tools))
            return tools
        except Exception as e:
            print('Error fetching tools', str(e))
            raise e

    @staticmethod
    def get_tool_agents(access_token: str, id: str) -> list[int]:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('agent_mcp_tool').select('*').eq('mcp_tool_id', id).execute()
            tool_agents = [item['agent_id'] for item in result.data if 'agent_id' in item]
            return tool_agents
        except Exception as e:
            print('Error fetching tool agents', str(e))
            raise

    @staticmethod
    def set_tool_agents(access_token: str, id: str, agent_ids: list[int]) -> list[int]:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            for agent_id in agent_ids:
                # Check if agent is valid and exists in the database
                agent_result = supabase.table('agents').select('*').eq('id', agent_id).limit(1).execute()
                if not agent_result.data:
                    print(f"Agent with ID {agent_id} does not exist.")
                    continue
                # Insert the agent-tool relationship
                supabase.table('agent_mcp_tool').insert({'mcp_tool_id': id, 'agent_id': agent_id}).execute()
            print('Inserted tool agents', agent_ids)
            return agent_ids
        except Exception as e:
            print('Error setting tool agents', str(e))
            raise