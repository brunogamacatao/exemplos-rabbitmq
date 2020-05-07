import pika

RABBITMQ_HOST = 'localhost'

params     = pika.ConnectionParameters(RABBITMQ_HOST)
connection = pika.BlockingConnection()
channel    = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print("[x] Enviado 'Hello World!'")

connection.close()