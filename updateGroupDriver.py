from method.sparkGroupId import sparkGroupId
from method.logstashGroupId import logstashGroupId
from method.fileGroupId import fileGroupId
from hdfs.client import InsecureClient
from yarn_api_client import ResourceManager
from rediscluster import RedisCluster
import resources.serverInfo as serverInfo

if __name__ == "__main__":
    rc = RedisCluster(startup_nodes=serverInfo.redisCluster, decode_responses=True, password=serverInfo.redisPassword)
    rm = ResourceManager(service_endpoints=["http://" + serverInfo.masterA + ":8088", "http://" + serverInfo.masterB + ":8088"])
    conn = InsecureClient("http://" + serverInfo.masterA + ":50070;http://" + serverInfo.masterB + ":50070", user="hdfs")

    sparkUpdate = sparkGroupId(rc, rm, conn)
    logstashUpdate = logstashGroupId(rc)
    fileUpdate = fileGroupId(rc)

    print("Start to update spark app consumer group")
    sparkUpdate.update(serverInfo.redisKey)
    print("Start to update logstash app consumer group")
    logstashUpdate.update(serverInfo.redisKey)
    print("Start to update other app consumer group")
    fileUpdate.update(serverInfo.redisKey, "groupid")
    print("Group key update")