from rediscluster import RedisCluster

redisCluster = [
        {"host": "localhost", "port": "6379"}
]
redisPassword = "password"

rc = RedisCluster(startup_nodes=redisCluster, decode_responses=True, password=redisPassword)
rc.delete('{ConsumerGroupMonitor}')