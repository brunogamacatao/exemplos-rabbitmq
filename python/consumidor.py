import pika

RABBITMQ_HOST = 'localhost'

params     = pika.ConnectionParameters(RABBITMQ_HOST)
connection = pika.BlockingConnection()
channel    = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Mensagem recebida: %r" % body)

channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Aguardando mensagens. Para sair, pressione CTRL+C')
channel.start_consuming()