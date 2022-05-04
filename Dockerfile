FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

RUN pip install -r requirements.txt
WORKDIR /app

ENTRYPOINT ["python3","multiObjectTracking.py","--json","development_assets/initial_conditions.json","--video","development_assets/input.mkv","--tracker","MEDIANFLOW"]

