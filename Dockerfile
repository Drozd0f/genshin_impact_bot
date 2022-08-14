FROM python:3
WORKDIR rater/
RUN apt -y update && apt -y upgrade && apt install -y tesseract-ocr
RUN wget https://github.com/tesseract-ocr/tessdata/blob/main/rus.traineddata && mv -v rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
RUN pip install watchdog[watchmedo]
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
