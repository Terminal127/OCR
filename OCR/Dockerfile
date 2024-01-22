FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install flask pytesseract Pillow



COPY . .

RUN pip install --ignore-installed -r ./requirements.txt

EXPOSE 80

CMD ["python3", "imageconv.py"]
