# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /appdata/claude

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and .env file to the working directory
COPY bot.py .
COPY .env .

# Run the bot script when the container starts
CMD ["python", "bot.py"]
