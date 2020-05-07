import time
import pika

RABBITMQ_HOST = 'localhost'
QUEUE = 'tarefas'

params     = pika.ConnectionParameters(RABBITMQ_HOST)
connection = pika.BlockingConnection()
channel    = connection.channel()

channel.queue_declare(queue=QUEUE, durable=True)

def callback(ch, method, properties, body):
    print(" [x] Recebido %r - Trabalhando na tarefa..." % body)
    time.sleep(body.count(b'.'))
    print(" [x] Pronto")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)

print(' [*] Aguardando mensagens. Para sair, pressione CTRL+C')
channel.start_consuming()