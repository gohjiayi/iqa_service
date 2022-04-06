# uvicorn main:app
from email.mime import multipart
from pathlib import Path
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.model import IQAModel
from app.models.result import IQAResult
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
    return templates.TemplateResponse("home.html", {"request": request})

'''
The path operation decorator applies to the function below it.
In this case, the decorator tells FastAPI that the function below corresponds to the path "/submitform" ,with an operation "post". 
There are several parameters that you can pass to your path operation decorator to configure it. 
Notice that these parameters are passed directly to the path operation decorator, not to your path operation function.
'''
'''
@app.post("/submitform")#, response_class=IQAResult)
async def handle_form(image: UploadFile = Form(...)):
    print("IN HANDLE FORM")
    print("image", image)
    file_name = os.path.join(os.getcwd()+"images"+image.filename.replace(" ", "-"))
    with open(file_name,'wb+') as f:
        uploaded = image.file.read()
        # print("uploaded", type(uploaded), uploaded[:50]) # uploaded <class 'bytes'> b'\x89PNG\r\n\x1
        f.write(uploaded)
    
    model: IQAModel = app.state.model
    prediction = model.predict(file_name)
    return {"prediction":prediction}
'''
@app.post("/submitform")#, response_class=IQAResult)
async def handle_form(request:Request, image: UploadFile = File(...)):
    print("IN HANDLE FORM")
    print("image", image)
    contents = await image.read()
    filename= image.filename
   
    model: IQAModel = app.state.model
    prediction = model.predict(contents)
    return {"prediction":prediction}

    # TODO SHOW the uploaded img and examples of each quality for video --> fyp summarization during presentation 
    # return {"filename": file_name}

'''
Note: When you access the url on the browser, you should get the following response "{"detail":"Method Not Allowed"}". 
This means two things: 1) your API is running fine. 
2) This message is coming because the method allowed on this URL is only POST. 
So the image can be uploaded by tools like postman or using some http client. 
There is a file "client.py" that can do the job of uploading the image as well.
Otherwise, the api can be accessed by http://127.0.0.1:8000/docs.
'''