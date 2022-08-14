COMPOSE ?= docker-compose -f docker-compose.yml

run:
	$(COMPOSE) up --build --force-recreate -d

rm:
	$(COMPOSE) rm -sfv

log:
	$(COMPOSE) logs -f muzlag

#$ sudo apt install tesseract-ocr
#$ sudo apt install libtesseract-dev

install_tesseract:
	sudo apt install tesseract-ocr

install_rus_language:
	wget https://github.com/tesseract-ocr/tessdata/blob/main/rus.traineddata
	sudo mv -v rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
