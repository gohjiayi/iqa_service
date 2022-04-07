# uvicorn main:app
from email.mime import multipart
from pathlib import Path
from pipes import Template
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.model import IQAModel
from app.services.event_handlers import start_app_handler, stop_app_handler
import os
os.system("pip install -U python-multipart")

APP_NAME = "Image Quality Assessment using DeepBIQ"
def get_app() -> FastAPI:
    fast_app = FastAPI(title=APP_NAME, debug=True)
    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))
    return fast_app

app = get_app()

app.mount(
    "/app/htmldirectory",
    StaticFiles(directory="app/htmldirectory"),
    name="static",
)

templates = Jinja2Templates(directory="app/htmldirectory")

@app.get("/", response_class=HTMLResponse)
def write_home(request: Request):
    prediction = "No prediction yet"
    return templates.TemplateResponse("home.html", {"request": request, "result":prediction})

'''
The path operation decorator applies to the function below it.
In this case, the decorator tells FastAPI that the function below corresponds to the path "/submitform" ,with an operation "post". 
There are several parameters that you can pass to your path operation decorator to configure it. 
Notice that these parameters are passed directly to the path operation decorator, not to your path operation function.
'''


# @app.post("/submitform", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def handle_form(request:Request):#, image: UploadFile = File(...)):
    print("IN HANDLE FORM OF main.py")
    form = await request.form()
    upload_file = form["image"]  # starlette.datastructures.UploadFile - not used here, but just for illustrative purposes
    filename = upload_file.filename  # str
    print("filename", filename)
    contents = await upload_file.read()  # bytes
    print("contents", contents[:50])
    content_type = upload_file.content_type  # str
    print("content_type", content_type)
   
    model: IQAModel = app.state.model
    prediction = model.predict(contents)
    return templates.TemplateResponse("home.html", {"request": request, "result":prediction})

'''
Note: When you access the url on the browser, you should get the following response "{"detail":"Method Not Allowed"}". 
This means two things: 1) your API is running fine. 
2) This message is coming because the method allowed on this URL is only POST. 
So the image can be uploaded by tools like postman or using some http client. 
There is a file "client.py" that can do the job of uploading the image as well.
Otherwise, the api can be accessed by http://127.0.0.1:8000/docs.
'''