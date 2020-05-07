import sys
import pika

RABBITMQ_HOST = 'localhost'
QUEUE = 'tarefas'

params     = pika.ConnectionParameters(RABBITMQ_HOST)
connection = pika.BlockingConnection()
channel    = connection.channel()

channel.queue_declare(queue=QUEUE, durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange = '',
                      routing_key = QUEUE,
                      body = message,
                      properties = pika.BasicProperties(
                         delivery_mode = 2, # mensagens persistentes
                      ))
print(" [x] Enviado %r" % message)

connection.close()