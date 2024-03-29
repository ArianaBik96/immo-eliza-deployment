# Use the official Python image as a base image
FROM python:3.12

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the app.py directly to the root directory of the container
COPY app.py .

# Set the environment variable for the port your app runs on
ENV PORT=8502

# Expose the port your Streamlit app runs on
EXPOSE $PORT

# Command to run the application
CMD [ "streamlit", "run", "--server.port", "8502", "app.py" ]