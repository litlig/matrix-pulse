# Using a slim version for a smaller base image
FROM mcr.microsoft.com/devcontainers/python:1-3.10-bullseye

RUN apt-get clean && apt-get update && apt-get install -y \
    python-dev \
    librocksdb-dev \
    rocksdb-tools \
    libgflags-dev \
    libsnappy-dev \
    zlib1g-dev \
    libbz2-dev \
    liblz4-dev \
    libzstd-dev 

RUN pip install Cython==0.29.21
RUN pip install python-rocksdb
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy just the requirements first
COPY ./requirements.txt .

# Upgrade pip
#RUN pip install --upgrade pip

# Increase timeout to wait for the new installation
RUN pip install -r requirements.txt

WORKDIR /code
# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000 --workers 1