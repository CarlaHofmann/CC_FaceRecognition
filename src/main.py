import os

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.background import BackgroundTask, BackgroundTasks
from starlette.responses import HTMLResponse

import FaceRecognition


api = FastAPI()
templates = Jinja2Templates(directory="templates")


def cleanup(path: str) -> None:
    os.remove(path)


@api.get('/', response_class=HTMLResponse)
def index():
    return FileResponse('templates/home.html')


@api.post('/submit', response_class=HTMLResponse)
async def upload_image(request: Request, bg_tasks: BackgroundTasks, img: UploadFile = File(...)):
    image_path = f"images/{img.filename}"
    with open(image_path, "wb+") as file_object:
        file_object.write(img.file.read())
    fr_image_path = FaceRecognition.face_detect(image_path, img.filename)
    bg_tasks.add_task(cleanup, image_path)
    bg_tasks.add_task(cleanup, fr_image_path)
    return templates.TemplateResponse('response.html',
                                      {'request': request, 'fr_image_path': fr_image_path},
                                      background=bg_tasks)


uvicorn.run(api)
