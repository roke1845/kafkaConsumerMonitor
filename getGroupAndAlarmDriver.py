import logging, json, time
import resources.serverInfo as serverInfo
import resources.esmapping as esmapping
from datetime import datetime
from rediscluster import RedisCluster
from utils.ESConnection import ESConnection
from utils.apiParser import apiParser
from utils.logMessage import logMessage

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
interval = 1800


def infoMessage(appName, group, status):
    return "App: " + appName + " Group: " + group + " status is " + status + " Alert"

def onlySend(body):
    ESConnection(serverInfo.esUrl.split(","), serverInfo.esUsername, serverInfo.esPassword).send("consumergroup_monitor", body, esmapping.mapping)
    logging.warning(infoMessage(body.get("appname"), body.get("status").get("group"), body.get("status").get("status")))

# def sendAndDel(body, rc):
#     ESConnection(serverInfo.esUrl.split(","), serverInfo.esUsername, serverInfo.esPassword).send("consumergroup_monitor", body, esmapping.mapping)
#     rc.hdel("{ConsumerGroupMonitor}", body['appname'])
#     logging.warning(infoMessage(body['status']['group'], body['status']['status']))


# def checkAndSend(body, topics):
#     topic = body.get("status").get("maxlag").get("topic")
#     if topic not in topics:
#         logging.info(body['status']['group'] + " not lag")
#     else:
#         onlySend(body)
#     # # in Docker, .timestamp() will get UTC+8 timestamp
#     # if (int(body['@timestamp'].timestamp()) - int(body['status']['maxlag']['end']['timestamp']/1000)) > 86400:
#     #     onlySend(body)
#     # else:
#     #     logging.info(body['status']['group'] + " not lag")

# def chekcStatusStatus(body, rc):
#     bodyStatus = body['status']['status']
#     switcher = {
#     'NOTFOUND': lambda: sendAndDel(body, rc)
#     }.get(bodyStatus, lambda: onlySend(body))
#     #.get(status_status, lambda: chekcStatusMaxlagStatus(body, rc))
#     switcher()
#
# def chekcStatusMaxlagStatus(body, status, topics):
#     topic = body.get("status").get("maxlag").get("topic")
#     if status != "OK" and topic not in topics:
#         onlySend(body)
#     else:
#         logging.info(body['status']['group'] + " not lag")
#
#     # maxlagStatus = body['status']['maxlag']['status']
#     # switcher = {
#     # 'OK': lambda: logging.info(body['status']['group'] + " not lag"),
#     # 'ERR': lambda: checkAndSend(body),
#     # 'STOP': lambda: checkAndSend(body),
#     # 'WARN': lambda: checkAndSend(body),
#     # 'STALL': lambda: checkAndSend(body)
#     # }.get(maxlagStatus, lambda: onlySend(body))
#     # switcher()

def checkStatus(body, status, topics=None):
    if status == "OK":
        logging.info("App: " + body.get("appname") + " Group: " + body.get("status").get("group") + " not lag")

    elif status == "NOTFOUND":
        onlySend(body)

    else:
        topic = body.get("status").get("maxlag").get("topic")
        if topic in topics:
            onlySend(body)
        else:
            logging.info("App: " + body.get("appname") + " Group: " + body.get("status").get("group") + " not lag")

if __name__=='__main__':
    rc = RedisCluster(startup_nodes=serverInfo.redisCluster, decode_responses=True, password=serverInfo.redisPassword)
    while True:
        try:
            keys = rc.hgetall(serverInfo.redisKey)
            for key, groupAndTopics in keys.items():
                try:
                    groupAndTopics = json.loads(groupAndTopics)
                    groupId = list(groupAndTopics.keys())[0]
                    topics = list(groupAndTopics.values())[0].split(",")
                    body = apiParser().getRestAPIToJson(serverInfo.burrowUrl + groupId + "/status")
                    body['@timestamp'] = datetime.utcnow()
                    body['appname'] = key
                    maxlag = body.get("status").get("maxlag", {})
                    if maxlag:
                        checkStatus(body, maxlag.get("status"), topics)
                    else:
                        checkStatus(body, body.get("status").get("status"), topics)
                except:
                    # logging.error("error key: " + key)
                    body = {
                        "appname": key,
                        "@timestamp": datetime.utcnow(),
                        "status": {
                            "cluster": "prod",
                            "group": "NOTFOUND",
                            "status": "NOTFOUND",
                            "complete": 1,
                            "partitions": [],
                            "partition_count": 0,
                            "maxlag": None,
                            "totallag": 0
                        }
                    }
                    onlySend(body)
        except:
            logMessage().printException()

        time.sleep(int(interval))