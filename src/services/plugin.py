
class Plugin(BaseModel):
    plugin: PluginModel

    def to_dict(self) -> dict:
        return self.plugin.to_dict()
    
    @staticmethod
    def get_plugin(name: str) -> PluginModel:
        try:
            result = supabase.table('plugins').select('*').eq('name_for_model', name).limit(1).single().execute()
            plugin = PluginModel.from_table(result.data)
            return plugin
        except Exception as e:
            print('Error getting plugin', str(e))
            raise e