FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3
RUN  apt-get -y install ffmpeg
RUN python3 -m pip install --upgrade pip
RUN pip install -U discord.py
RUN pip install -U python-dotenv 
RUN pip install -U pika
RUN pip install -U youtube-dl
RUN pip install google-api-python-client   

RUN pip install pafy
RUN pip install pydub
RUN pip install PyNaCl



ENV PYTHONUNBUFFERED=TRUE

COPY . discord_listener/

CMD ["python","discord_listener/bot.py"]
