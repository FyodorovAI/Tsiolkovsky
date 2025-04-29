import pytest
from models.health_check import HealthStatusTypes, HealthUpdateModel
from pydantic import HttpUrl, ValidationError


def get_default_hc(
    tool_id: str | None = "5",
    health_status: HealthStatusTypes = "healthy",
    api_url: HttpUrl | None = HttpUrl("http://www.example.com"),
) -> HealthUpdateModel:

    try:
        hc = HealthUpdateModel(
            tool_id=tool_id, health_status=health_status, api_url=api_url
        )
    except ValidationError as e:
        print("Health update model validation error:", e)
        raise
    else:
        print("Health update model:", hc)
        return hc


def test_default_hc_validation():
    try:
        get_default_hc()
    except Exception as e:
        assert False, f"An exception occurred: {e}"
    else:
        assert True, "No exception should be thrown"


def test_invalid_hc_validation():
    try:
        get_default_hc(health_status="invalid")
    except Exception as e:
        assert True, f"An exception should be thrown: {e}"
    else:
        assert False, "An exception should be thrown"


def test_invalid_tool_id():
    try:
        get_default_hc(tool_id=5)
    except Exception as e:
        assert True, f"An exception should be thrown: {e}"
    else:
        assert False, "An exception should be thrown"


def test_invalid_api_url():
    invalid_urls = ["invalid-url", "ftp://invalid-url", "localhost:8000"]
    for invalid_url in invalid_urls:
        try:
            print(f"Testing invalid URL: {invalid_url}")
            get_default_hc(api_url=invalid_url)
        except Exception as e:
            assert True, f"An exception should be thrown for {invalid_url}: {e}"
        else:
            assert False, "An exception should be thrown"
