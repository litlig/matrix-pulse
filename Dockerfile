# Using a slim version for a smaller base image
FROM python:3.11.6-slim-bullseye@sha256:0c1fbb294096d842ad795ee232d783cab436c90b034210fe894f2bb2f2be7626

RUN apt-get clean && apt-get update && apt-get install -y \
    git \
    curl
#  zlib1g-dev libbz2-dev liblz4-dev libzstd-dev

ENV PATH="/root/.cargo/bin:${PATH}"

# Copy just the requirements first
COPY ./requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Increase timeout to wait for the new installation
RUN pip install --no-cache-dir -r requirements.txt --timeout 200

WORKDIR /code
# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --workers 1