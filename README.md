# API Milvus Lite

An restful api for milvus lite to be used outside python ecosystem!

Consume this api to use milvus lite with any other stack and secure ownership of its data!

## Installation

You can use with docker container via docker compose:

```yaml
version: '3.8'

services:
  milvus:
    image: kesc23/milvus-lite:1.0.0
    environment:
      - ENV_PRODUCTION="true"
    ports:
      - "19530:19530"
    volumes:
      - ./volumes/data:/home/ubuntu/milvus_lite/data
```
