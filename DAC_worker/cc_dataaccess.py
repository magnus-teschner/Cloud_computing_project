import pika
import json
import cc_functions


class MessageProcessor:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='my_queue')
        self.channel.queue_declare(queue='response_queue')

        self.db_access = cc_functions.DbAccess()

        self.channel.basic_consume(queue='my_queue', on_message_callback=self.process_message, auto_ack=False)

    def process_message(self, ch, method, properties, body):
        input_data = json.loads(body.decode('utf-8')) # Jetzt verwenden wir json.loads um den JSON String zu decodieren

        name = input_data['name']
        discount = input_data['discount']
        products = input_data['products']

        # Benutzer erstellen oder aktualisieren
        self.db_access.insert_customer(name, discount)

        for product in products:
            product_name = product['name']
            product_price = product['price']

            # Produkte einfügen
            self.db_access.insert_product(product_name, product_price)

            # Verkaufsinformationen einfügen
            self.db_access.insert_sale(name, product_name)

        response = f"Successfully processed the message for customer {name}"

        self.channel.basic_publish(
            exchange='',
            routing_key='response_queue',
            body=response
        )

        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.start_consuming()

    def __del__(self):
        self.connection.close()


if __name__ == '__main__':
    message_processor = MessageProcessor()
    message_processor.start_consuming()
