from pydantic import BaseModel, EmailStr, HttpUrl
from typing import TypeVar
import re
from typing import Literal

APIUrlTypes = Literal['openapi']

MAX_NAME_LENGTH = 80
MAX_DESCRIPTION_LENGTH = 280
VALID_CHARACTERS_REGEX = r'^[a-zA-Z0-9\s.,!?:;\'"-]+$'

class ToolModel(BaseModel):
    name_for_human: str
    name_for_ai: str
    description_for_human: str
    description_for_ai: str
    api_type: APIUrlTypes
    api_url: HttpUrl
    logo_url: HttpUrl
    contact_email: EmailStr
    legal_info_url: HttpUrl

    def validate(self) -> bool:
        try:
            ToolModel.validate_name_for_human(self.name_for_human)
            ToolModel.validate_name_for_ai(self.name_for_ai)
            ToolModel.validate_description_for_human(self.description_for_human)
            ToolModel.validate_description_for_ai(self.description_for_ai)
        except ValueError as e:
            print("Tool model validation error:", e)
            return False
        else:
            return True

    def to_dict(self) -> dict:
        return {
            'name_for_human': self.name_for_human,
            'name_for_ai': self.name_for_ai,
            'description_for_human': self.description_for_human,
            'description_for_ai': self.description_for_ai,
            'api_type': self.api_type,
            'api_url': str(self.api_url),
            'logo_url': str(self.logo_url),
            'contact_email': str(self.contact_email),
            'legal_info_url': str(self.legal_info_url)
        }

    @staticmethod
    def validate_name_for_human(name_for_human: str) -> str:
        if not name_for_human:
            raise ValueError('Name for human is required')
        if len(name_for_human) > MAX_NAME_LENGTH:
            raise ValueError('Name for human exceeds maximum length')
        if not re.match(VALID_CHARACTERS_REGEX, name_for_human):
            raise ValueError('Name for human contains invalid characters')
        return name_for_human

    @staticmethod
    def validate_name_for_ai(name_for_ai: str) -> str:
        if not name_for_ai:
            raise ValueError('Name for AI is required')
        if len(name_for_ai) > MAX_NAME_LENGTH:
            raise ValueError('Name for AI exceeds maximum length')
        if not re.match(VALID_CHARACTERS_REGEX, name_for_ai):
            raise ValueError('Name for AI contains invalid characters')
        return name_for_ai

    @staticmethod
    def validate_description_for_human(description_for_human: str) -> str:
        if not description_for_human:
            raise ValueError('Description for human is required')
        if len(description_for_human) > MAX_DESCRIPTION_LENGTH:
            raise ValueError('Description for human exceeds maximum length')
        if not re.match(VALID_CHARACTERS_REGEX, description_for_human):
            raise ValueError('Description for human contains invalid characters')
        return description_for_human

    @staticmethod
    def validate_description_for_ai(description_for_ai: str) -> str:
        if not description_for_ai:
            raise ValueError('Description for AI is required')
        if len(description_for_ai) > MAX_DESCRIPTION_LENGTH:
            raise ValueError('Description for AI exceeds maximum length')
        if not re.match(VALID_CHARACTERS_REGEX, description_for_ai):
            raise ValueError('Description for AI contains invalid characters')
        return description_for_ai