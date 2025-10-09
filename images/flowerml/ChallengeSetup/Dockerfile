# Use our provided base image.
# You can also use your own base image if you need to, but make sure it has all the dependencies installed and is publicly available.
FROM registry.gitlab.com/nct_tso_public/challenge-docker:latest

# set working directory
WORKDIR /app

# Install additional dependencies, if you need any on top of the base image. e.g. opencv
#RUN apt-get update && apt-get install -y \
#    opencv-python

# Install additional dependencies, if you need any on top of the base image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Run prepare.py to e.g. download pretrained models
COPY prepare.py .
RUN python3 prepare.py
RUN rm prepare.py

# copy code from host to container
WORKDIR /app/code
COPY src/ .

# execute main.py
CMD ["python3", "main.py"]