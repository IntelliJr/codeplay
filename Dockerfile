# Use an official Python runtime as a parent image
FROM python:3.10.4-alpine

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Register user_solutions as module
ENV PYTHONPATH "/code/user_solutions/:/code/user_solutions/solutions/"

# Executing the run statement that will install our compilers and add packages in requirements.txt
RUN apk update && \
    apk add --no-cache gcc musl-dev g++ && \
    rm -rf /var/cache/apk/* && \
    pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
