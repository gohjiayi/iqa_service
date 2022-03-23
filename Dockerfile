# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM nvcr.io/nvidia/pytorch:21.07-py3

# Copy contents
COPY ./requirements.txt /requirements.txt
# COPY ./app/run.sh /run.sh

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD cd / && sh /run.sh