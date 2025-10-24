# Dockerfile

FROM python:3.12-slim

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# set working directory
WORKDIR /code

# install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy project
COPY ./app /code/app
COPY ./models /code/models

# Add User
RUN useradd -m myuser
USER myuser

# expose port
EXPOSE $PORT

# run server
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT