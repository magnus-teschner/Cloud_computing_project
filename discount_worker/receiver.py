#!/usr/bin/env python
import pika, sys, os, json

def apply_discount(order: dict) -> dict:
    total_price = 0
    for element in order["content"]:
        element["price"] = round(float(element["price"]) * (100-int(order["discount"]))/100, 2)
        total_price += element["price"]
    order["total_price"] = total_price
    return order

def send_in_que(body: dict, queue_name: str, channel) -> None:
    channel.basic_publish(exchange='', routing_key=queue_name, body=body)

def body_in_dict(body: bytes) -> dict:
    body_str = body.decode("utf-8")
    return json.loads(body_str)

def create_connection_channel(host: str, port: int, queue_name: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port = port))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    return channel


def main() -> None:
    
    #parameters
    host1 = os.environ['HOST1']
    port1 = os.environ['PORT1']
    queue_name1 = os.environ['QUEUE_NAME_1']

    host2 = os.environ['HOST2']
    port2 = os.environ['PORT2']
    queue_name2 = os.environ['QUEUE_NAME_2']
    

    #queue 1
    channel1 = create_connection_channel(host1, port1, queue_name1)

    #queue 2
    channel2 = create_connection_channel(host2, port2, queue_name2)


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        dict_body = body_in_dict(body)
        body_with_discount = apply_discount(dict_body)
        send_in_que(json.dumps(body_with_discount), queue_name2, channel2)

    channel1.basic_consume(queue=queue_name1, on_message_callback=callback, auto_ack=True)
    channel1.start_consuming()

if __name__ == '__main__':
    main()