import pytest
from starlette import status

pytestmark = pytest.mark.asyncio
APP_URL: str = "/ping_application"
DATABASE_URL: str = "/ping_database"


class TestCheckHealthApp:
    async def test_check_health_app(self, client):
        response = await client.get(url=APP_URL)
        assert response.status_code == status.HTTP_200_OK

    async def test_check_health_database(self, client):
        response = await client.get(url=DATABASE_URL)
        assert response.status_code == status.HTTP_200_OK
