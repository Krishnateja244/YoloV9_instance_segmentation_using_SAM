FROM python:3.10

WORKDIR /

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python","./app.py"]

