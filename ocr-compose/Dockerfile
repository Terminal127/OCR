# Use a minimal Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install Tesseract and other dependencies
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install flask pytesseract Pillow

# Copy the Flask application files to the container
COPY . .

RUN pip install -r ./requirements.txt
# Expose the default Flask port
EXPOSE 8000

# Run the Flask application
CMD ["python3", "./app/imageconv.py"]
