from fastapi import FastAPI
from starlette import status
from starlette.responses import Response

from models import Body

app = FastAPI()  # noqa: pylint=invalid-name

@app.post("/release/")
async def release(*,
                  body: Body,
                  chat_id: str = None):
    await proceed_release(body, chat_id)
    return Response(status_code=status.HTTP_200_OK)
