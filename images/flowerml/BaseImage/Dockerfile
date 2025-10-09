FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directories, content will be mounted from host
RUN mkdir code  # code to execute, contains main.py
RUN mkdir input  # input data to read
RUN mkdir output  # output data to write

WORKDIR /app/code

# default command to execute
CMD ["python3", "main.py"]