# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM nvcr.io/nvidia/pytorch:21.07-py3

# Copy contents
COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./deepbiq_deploy /deepbiq_deploy
#  The first thing a build process does is send the entire context (recursively) to the daemon. In most cases, it’s best to start with an empty directory as context and keep your Dockerfile in that directory. Add only the files needed for building the Dockerfile.
# To use a file in the build context, the Dockerfile refers to the file specified in an instruction, for example, a COPY instruction.

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD cd / && sh /app/run.sh