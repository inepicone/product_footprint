# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY eco_impact.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the script
CMD ["python", "eco_impact.py"]
