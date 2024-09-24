FROM python:3.12.6-slim

WORKDIR /home/ubuntu

RUN mkdir milvus_lite

COPY . ./milvus_lite

WORKDIR /home/ubuntu/milvus_lite

RUN pip install -r requirements.txt

EXPOSE 19530

ENTRYPOINT [ "python", "app.py" ]