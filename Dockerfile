FROM python:3
WORKDIR rater/
RUN apt -y update && apt -y upgrade && apt install -y tesseract-ocr python3-opencv tesseract-ocr-rus
RUN pip install watchdog[watchmedo]
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
