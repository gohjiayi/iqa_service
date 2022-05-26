# Important source files
* app/htmldirectory: This app is mounted in app/main.py
    * home.html: Defines the image upload form (POST method)
    * style.css: Defines how the page looks
    * upload.js: Defines how the image preview appears after uploading
* app/main.py: Defines the FastAPI app that renders the HTML, initializes the model, handles the input of the uploaded image into the model, and returns the model prediction. 
* app/run.sh: Start the FastAPI app using Uvicorn
* models/model.py: Defines the DeepBIQ model (PyTorch CNN + sklearn SVR) and how the uploaded image is passed through the model to generate the final prediction
* services/event_handler.py: Load the CNN and SVR upon app launch
* deepbiq_deploy: Contains trained CNN and SVR weights, as well as MOS scores of the combined dataset in order for us to scale the model predictions to a percentile later (more easy to interpret)
* Dockerfile: Container with all dependencies installed; runs run.sh to start the FastAPI app
* deepbiq.sh: Pull the Docker image

# Running instructions
* Build and push image with `t=phoebezhouhuixin/iqa_service:latest && sudo docker build -t $t . && sudo docker push $t`
* Run deepbiq.sh with `sudo sh deepbiq.sh`
    * deepbiq.sh specifies a volume map between the source files in the local directory (./app) and the Docker container's directory (/app). Thus, any changes made to main.py locally will be reflected automatically in the Docker container.
* Go to http://0.0.0.0:8000/ (localhost port 8000)
