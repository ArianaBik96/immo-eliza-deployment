# Use an official Python runtime as the base image
FROM python:3.12.2

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit runs on
EXPOSE 8502

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]