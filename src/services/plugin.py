from pydantic import BaseModel
from models.plugin import PluginModel
from fyodorov_utils.config.supabase import get_supabase

supabase = get_supabase()

class Plugin(PluginModel):    

    @staticmethod
    def get_plugin(name: str) -> 'Plugin':
        try:
            result = supabase.table('plugins').select('*').eq('name_for_model', name).limit(1).single().execute()
            plugin = PluginModel.from_table(result.data)
            return Plugin(**plugin.dict())
        except Exception as e:
            print('Error getting plugin', str(e))
            raise e