FROM python:3.10-slim

# Install ffmpeg
RUN apt update && apt install -y ffmpeg

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
