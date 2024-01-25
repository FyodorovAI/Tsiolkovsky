from pydantic import BaseModel, HttpUrl
import re
from typing import Literal

HealthStatusTypes = Literal['healthy', 'unhealthy', 'down', 'unknown', 'authentication_error']

class HealthUpdateModel(BaseModel):
    tool_id: str
    api_url: HttpUrl | None
    health_status: HealthStatusTypes

    def to_dict(self) -> dict:
        return {
            "tool_id": self.tool_id,
            "health_status": self.health_status,
            "extra": {
                "api_url": str(self.api_url)
            }
        }
