# Set base image (host OS)
FROM python:3.12-alpine

# By default, listen on port 5000
EXPOSE 8000/tcp

# Set the working directory in the container
WORKDIR /app

# Install git
RUN apk update && apk add git

# Go into working directory
RUN pip install --upgrade pip

## Install any dependencies
RUN pip install git+https://github.com/a96tudor/elections-maps.git

COPY app.py .
COPY election_maps ./election_maps
COPY tmp/aws_creds /root/.aws/credentials


# Specify the command to run on container start
CMD [ "python", "app.py" ]
