FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3

RUN pip install pika
RUN pip install wikipedia
ENV PYTHONUNBUFFERED 1


COPY ./manager.py ./manager.py

CMD ["python", "manager.py"]