# coding: utf-8
import sys
import pika
import uuid

RABBITMQ_HOST = 'localhost'
RPC_QUEUE     = 'rpc_queue'

class FibonacciRpcClient(object):
  def __init__(self, host = RABBITMQ_HOST):
    # Conecta
    self.connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=host))

    # Obtém um canal de comunicação com o RabbitMQ
    self.channel = self.connection.channel()

    # Cria uma fila de resposta
    result = self.channel.queue_declare(queue='', exclusive=True)
    self.callback_queue = result.method.queue

    # Associa o método de callback com a fila de resposta
    self.channel.basic_consume(
      queue = self.callback_queue,
      on_message_callback = self.on_response,
      auto_ack = True)

  # Esse método vai ser chamado sempre que chegar uma resposta
  def on_response(self, ch, method, props, body):
    if self.corr_id == props.correlation_id: # só aceita a resposta com o id do produtor correto
      self.response = body

  # Esse é o método que deve ser chamado para criar uma tarefa
  def call(self, n):
    self.response = None
    self.corr_id = str(uuid.uuid4())    # id do produtor
    # Envia a tarefa ...
    self.channel.basic_publish(
      exchange='',                      # no exchange padrão
      routing_key=RPC_QUEUE,            # na fila rpc_queue
      properties=pika.BasicProperties(  # esses props são acessados no worker:
        reply_to = self.callback_queue, #   - a fila para onde enviar a resposta
        correlation_id = self.corr_id,  #   - o id do produtor
      ),
      body=str(n))                      # corpo da mensagem
    
    # loop para transformar essa chamada asíncrona em síncrona
    while self.response is None:            # enquanto não tem resposta ...
      self.connection.process_data_events() # espera por mensagens na fila de respostas

    return int(self.response) # retorna a resposta


fibonacci_rpc = FibonacciRpcClient()
n = int(sys.argv[1])
print(" [x] Solicitando fib(%s) ..." % n)
response = fibonacci_rpc.call(n)
print(" [.] Resultado %r" % response)