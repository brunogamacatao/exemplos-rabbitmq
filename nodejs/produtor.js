const amqp = require('amqplib');

const main = async () => {
  const conn = await amqp.connect('amqp://localhost');
  const channel = await conn.createChannel();

  const queue = 'hello';
  let msg = 'Hello world';

  channel.assertQueue(queue, { durable: false });
  channel.sendToQueue(queue, Buffer.from(msg));
  console.log(" [x] Sent %s", msg);

  setTimeout(() => { 
    conn.close(); 
    process.exit(0) 
  }, 500);    
};

main();