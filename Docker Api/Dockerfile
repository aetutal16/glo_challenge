# Use the official image for python
FROM python:3.11-slim

#Stablish the work directory inside the container
WORKDIR /app

# Install dependencies including postgreSQL 
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code to the container
COPY . .

# Use the port 5000, this is the port used by flask
EXPOSE 5000

# Command to execute the api
CMD ["python", "api.py"]