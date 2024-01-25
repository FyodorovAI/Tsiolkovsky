import pytest
from models.tool import ToolModel 
from pydantic import ValidationError

def get_default_tool(
        name_for_human="My Tool",
        name_for_ai="my-tool",
        description_for_human="This is my tool.",
        description_for_ai="This is my tool.",
        api_type="openapi",
        api_url="https://example.com/openapi.json",
        logo_url="https://example.com/logo.png",
        contact_email="I7JQK@example.com",
        legal_info_url="https://example.com/legal-info.pdf",
    ) -> ToolModel:

    try:
        tool = ToolModel(
            name_for_human=name_for_human,
            name_for_ai=name_for_ai,
            description_for_human=description_for_human,
            description_for_ai=description_for_ai,
            api_type=api_type,
            api_url=api_url,
            logo_url=logo_url,
            contact_email=contact_email,
            legal_info_url=legal_info_url,
        )
    except ValidationError as e:
        print("Tool model validation error:", e)
        raise
    else:
        print("Tool model:", tool)
        return tool

def test_default_tool_validation():
    # Get a tool by calling get_default_tool()
    tool = get_default_tool()

    # Validate the tool and get a boolean indicating if it is valid
    is_valid = tool.validate()

    assert is_valid, (
        "Default tool should be valid"
    )


def test_long_name_for_human():
    # Create a tool with a long name for human
    long_name_tool = get_default_tool(name_for_human="A" * 101)
    is_valid = long_name_tool.validate()
    assert not is_valid, "Long name for human should result in invalid tool"


def test_invalid_name_for_human():
    # Create a tool with an invalid name for human
    invalid_name_tool = get_default_tool(name_for_human="My Tool @!")
    is_valid = invalid_name_tool.validate()
    assert not is_valid, "Invalid name for human should result in invalid tool"


def test_long_description_for_human():
    # Create a tool with a long description for human
    long_description_tool = get_default_tool(description_for_human="A" * 1001)
    is_valid = long_description_tool.validate()
    assert not is_valid, "Long description for human should result in invalid tool"


def test_invalid_description_for_human():
    # Create a tool with an invalid description for human
    invalid_description_tool = get_default_tool(description_for_human="This is my tool @!")
    is_valid = invalid_description_tool.validate()
    assert not is_valid, "Invalid description for human should result in invalid tool"


def test_invalid_api_type():
    try:
        # Create a tool with an invalid api_type
        invalid_tool = get_default_tool(api_type="invalid")
    except ValidationError as e:
        assert isinstance(e, ValidationError), "Expected a Pydantic ValidationError"
    else:
        assert False, "Expected a Pydantic ValidationError"


def test_invalid_api_url():
    try:
        # Create a tool with an invalid api_url
        invalid_url_tool = get_default_tool(api_url="invalid-url")
    except ValidationError as e:
        assert isinstance(e, ValidationError), "Expected a Pydantic ValidationError"
    else:
        assert False, "Expected a Pydantic ValidationError"


def test_invalid_logo_url():
    try:
        # Create a tool with an invalid logo_url
        invalid_url_tool = get_default_tool(logo_url="invalid-url")
    except ValidationError as e:
        assert isinstance(e, ValidationError), "Expected a Pydantic ValidationError"
    else:
        assert False, "Expected a Pydantic ValidationError"


def test_invalid_contact_email():
    try:
        # Create a tool with an invalid contact_email
        invalid_email_tool = get_default_tool(contact_email="invalid-email")
    except ValidationError as e:
        assert isinstance(e, ValidationError), "Expected a Pydantic ValidationError"
    else:
        assert False, "Expected a Pydantic ValidationError"
