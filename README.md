# API Milvus Lite

An restful api for milvus lite to be used outside python ecosystem!

Consume this api to use milvus lite with any other stack and secure ownership of its data!

## v2 Features

![Collectrions - Working](https://img.shields.io/static/v1?label=Collections&message=Working&color=2ea44f&logo=milvus)
![Vectors - Working](https://img.shields.io/static/v1?label=Vectors&message=Working&color=2ea44f&logo=milvus)
![Alias - Planned](https://img.shields.io/badge/Alias-Planned-yellow?logo=milvus)
![Import - Planned](https://img.shields.io/badge/Import-Planned-yellow?logo=milvus)
![Index - Planned](https://img.shields.io/badge/Index-Planned-yellow?logo=milvus)
![Partition - Planned](https://img.shields.io/badge/Partition-Planned-yellow?logo=milvus)
![Role - Planned](https://img.shields.io/badge/Role-Planned-yellow?logo=milvus)
![User - Planned](https://img.shields.io/badge/User-Planned-yellow?logo=milvus)

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
