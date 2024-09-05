# Use a lightweight Python image


FROM openjdk:17.0.1-jdk-slim


RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y python3-pip
# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to /app in the container
COPY . /app

# Install Flask
RUN pip install flask

# Expose the port the app runs on
EXPOSE 5002

# Define the command to run the application
CMD ["python3", "app.py"]
