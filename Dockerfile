# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install setuptools

RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]