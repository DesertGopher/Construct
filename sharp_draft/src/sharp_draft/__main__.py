import uvicorn
from settings import settings


uvicorn.run(
    'sharp_draft.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)

