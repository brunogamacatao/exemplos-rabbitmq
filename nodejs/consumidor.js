const amqp = require('amqplib');

const main = async () => {
  const conn = await amqp.connect('amqp://localhost');
  const channel = await conn.createChannel();

  const queue = 'hello';

  channel.assertQueue(queue, { durable: false });
  channel.consume(queue, (msg) => {
    console.log(" [x] Received %s", msg.content.toString());
  }, {noAck: true});
};

main();