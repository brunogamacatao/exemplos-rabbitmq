# coding: utf-8
import pika

RABBITMQ_HOST = 'localhost'
RPC_QUEUE     = 'rpc_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()         # Obtém o canal de comunicação
channel.queue_declare(queue=RPC_QUEUE) # Cria a fila

# Implementação recursiva e lenta da sequência de Fibonacci
def fib(n):
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n - 1) + fib(n - 2)

# Função chamada sempre que uma solicitação chegar
def on_request(ch, method, props, body):
  n = int(body)

  print(" [.] Recebida uma requisição para calcular fib(%s)" % n)
  response = fib(n) # calcula o número de fibonacci

  # Envia a resposta
  ch.basic_publish(exchange='',             # exchance padrão
    routing_key=props.reply_to,             # fila da resposta
    properties=pika.BasicProperties(        # propriedades da mensagem
      correlation_id = props.correlation_id # o id do produtor da tarefa
    ),
    body=str(response))                     # a resposta em si
  ch.basic_ack(delivery_tag=method.delivery_tag) # acknowledgment

# O canal só vai receber 1 mensagem por vez
channel.basic_qos(prefetch_count=1)
# As requisições virão pela 'rpc_queue'
channel.basic_consume(queue=RPC_QUEUE, on_message_callback=on_request)

print(" [x] Aguardando requisições RPC ...")
channel.start_consuming()