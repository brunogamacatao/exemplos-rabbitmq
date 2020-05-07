const amqp = require('amqplib');

const main = async () => {
  const conn = await amqp.connect('amqp://localhost');
  const channel = await conn.createChannel();

  const queue = 'tarefas';

  channel.assertQueue(queue, { durable: true });
  channel.prefetch(1);

  console.log(" [x] Aguardando tarefas ...");
  channel.consume(queue, (msg) => {
    var secs = msg.content.toString().split('.').length - 1;

    console.log(" [x] Recebido %s", msg.content.toString());

    setTimeout(() => {
      console.log(" [x] Pronto!");
      channel.ack(msg);
    }, secs * 1000);
  }, {noAck: false});
};

main();