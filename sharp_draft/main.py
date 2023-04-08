import uvicorn
from settings import settings

from fastapi import FastAPI
from routers import router

tags_metadata = [
    {
        "name": "Products",
        "description": "Requests for handing with products.",
    },
    {
        "name": "Categories",
        "description": "Methods for requests connected with products categories.",
    },
    {
        "name": "News",
        "description": "Methods with organization's news.",
    },
]

app = FastAPI(
        openapi_tags=tags_metadata,
        title="FastApi service of Construct",
        version="0.1.2",
        description="Service for telegram bot"
    )

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )

