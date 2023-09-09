from config import settings

TORTOISE_ORM = {
    "connections": {"default": str(settings.postgres_url)},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}