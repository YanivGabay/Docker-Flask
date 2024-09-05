# Start with the official Dart image
FROM dart:stable as build

# Set up the environment variables
ENV PUB_CACHE=/usr/local/dart-pub-cache

# Update and install Python, pip, and Flask through the apt package manager
RUN apt-get update && \
    apt-get install -y software-properties-common python3-pip python3-flask

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to /app in the container
COPY . /app

# Expose the port the app runs on
EXPOSE 5003

# Define the command to run the application
CMD ["python3", "app.py"]
