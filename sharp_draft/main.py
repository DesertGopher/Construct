import uvicorn
from settings import settings

from fastapi import FastAPI
from routers import router


app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )

