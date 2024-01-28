from typing import Literal, TypedDict
from pydantic import BaseModel, HttpUrl

APIUrlTypes = Literal['openapi', 'graphql', 'graphql_ws', 'rest']
class AuthType(TypedDict):
    type: Literal["user_http", "oauth"] = "user_http"
    authorization_type: Literal["bearer"] = "bearer"

class APIType(TypedDict):
    type: APIUrlTypes = "openapi"
    url: HttpUrl
    has_user_authentication: bool

# example of a plugin output
output = {
    "schema_version": "v1",
    "name_for_model": "ai-plugin",
    "name_for_human": "Tool Name for Human",
    "description_for_model": "Tool Description for AI",
    "description_for_human": "Tool Description for Human",
    "auth": {
        "type": "user_http",
        "authorization_type": "bearer"
    },
    "api": {
        "type": "openapi",
        "url": "http://example.com",
        "has_user_authentication": false
    },
    "logo_url": "http://logo.url",
    "contact_email": "contact@example.com",
    "legal_info_url": "http://legal.info.url"
}

class PluginTableModel(BaseModel):
    name_for_model: str
    name_for_human: str
    description_for_model: str
    description_for_human: str
    api: APIType
    logo_url: str
    contact_email: str
    legal_info_url: str

class PluginModel(BaseModel):
    schema_version: str = "v1"
    auth: AuthType = AuthType()
    plugin: PluginTableModel

    def to_dict(self) -> dict:
        return {
            'schema_version': self.schema_version,
            'name_for_model': self.plugin.name_for_model,
            'name_for_human': self.plugin.name_for_human,
            'description_for_model': self.plugin.description_for_model,
            'description_for_human': self.plugin.description_for_human,
            'auth': self.auth,
            'api': self.plugin.api,
            'logo_url': self.plugin.logo_url,
            'contact_email': self.plugin.contact_email,
            'legal_info_url': self.plugin.legal_info_url
        }

    @staticmethod
    def from_table(plugin: dict) -> 'PluginModel':
        return PluginModel(plugin=PluginTableModel(**plugin))

