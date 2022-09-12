from app.endpoints.health_check import api_router as health_check_router

list_of_routes = [health_check_router]

__all__ = ['list_of_routes']
