import redis from 'redis';

const client = redis.createClient();

const hashKey = 'HolbertonSchools';

client.hset(hashKey, 'Portland', 50, redis.print);
client.hset(hashKey, 'Seattle', 80, redis.print);
client.hset(hashKey, 'New York', 20, redis.print);
client.hset(hashKey, 'Bogota', 20, redis.print);
client.hset(hashKey, 'Cali', 40, redis.print);
client.hset(hashKey, 'Paris', 2, redis.print);

client.hgetall(hashKey, (err, reply) => {
  console.log(reply);
});
