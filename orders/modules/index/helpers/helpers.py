import requests
from fastapi import HTTPException
import os
import json
from modules.index.request.request_index_dto import ParseProductDetails, ParseUserDetails
import pika
from time import sleep
from datetime import datetime

parse_dicts = {
    'product-service': ParseProductDetails,
    'user-service': ParseUserDetails
}


async def fetch_data(service: str, url: str, timeout: int):
    try:
        response = requests.get(url=url, timeout=timeout)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503,
            detail=f'The {service} microservice timed out. Timeout is set to {timeout} seconds. Please try again later.'
        )
    if response.status_code == 200:
        try:
            return parse_dicts[service](**json.loads(response.content.decode('utf-8')))
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=503,
                detail=f'The {service} sent corrupted data. Please try again later.'
            )
    print('status_code',response.status_code,'content',response.content)
    raise HTTPException(
        status_code=503,
        detail=f'The {service} microservice did not return a 200 status. Please try again later.'
    )


async def send_data_to_rabbit_mq(exchange_name,routing_key,string_message_json):
    retries = 3
    sleep_time = 1
    for i in range(retries):
        print(datetime.now())
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=os.getenv('rabbitmq_host'),
                    port=int(os.getenv('rabbitmq_port')),
                    credentials=pika.PlainCredentials(
                        os.getenv('RABBITMQ_DEFAULT_USER'),
                        os.getenv('RABBITMQ_DEFAULT_PASS')
                    ),
                    socket_timeout=1
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue=routing_key)
            channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
            channel.queue_bind(exchange=exchange_name, queue=routing_key, routing_key=routing_key)
            channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=string_message_json)
            connection.close()
            return
        except Exception as e:
            sleep(sleep_time)
    rabbitmq_message ={
        'exchange': exchange_name,
        'routing_key': routing_key,
        'queue': routing_key,
        'message': string_message_json,
    }
    # I would log this and retry with a worker node like celery
    with open('message_broker_logs.txt','a') as log:
        log.write(f'{datetime.utcnow()} {json.dumps(rabbitmq_message)}\n')
