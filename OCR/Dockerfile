# Use a minimal Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install Tesseract and other dependencies
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install flask pytesseract Pillow

# Copy the Flask application files to the container
COPY imageconv.py .
COPY templates templates

# Expose the default Flask port
EXPOSE 80

# Run the Flask application
CMD ["python", "imageconv.py"]
