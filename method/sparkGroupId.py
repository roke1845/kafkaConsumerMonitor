import re, json
from utils.apiParser import apiParser
from pyhocon import ConfigFactory
from .groupIdUpdater import groupIdUpdater

class sparkGroupId(groupIdUpdater):
    def getConfPath(self, id, trackingUrl):
        try:
            envPlayload = apiParser().getRestAPIToJson("%sapi/v1/applications/%s/environment" % (trackingUrl, id))
            systemProperties = envPlayload['systemProperties']
            low = 0
            high = len(systemProperties) - 1
            while low <= high:
                mid = int((high + low) / 2)
                if "sun.java.command" == systemProperties[mid][0]:
                    return re.findall(r'/user/tmpForSpark.*\.conf', systemProperties[mid][1])[0]
                elif "sun.java.command" > systemProperties[mid][0]:
                    low = mid + 1
                else:
                    high = mid - 1
        except:
            return None

    def getGroupIdAndTopics(self, configPath):
        try:
            with self.HDFSConn.read(configPath) as reader:
                conf = ConfigFactory.parse_string(reader.read().decode())
                if "kafka" not in conf:
                    groupId = conf['Prd']['Kafka']['Consumer']['Group_Id']
                    topics = conf['Prd']['Kafka']
                elif "consumer" not in conf['kafka']:
                    groupId = conf['kafka']['groupId']
                    topics = conf['kafka']['topics']
                else:
                    groupId = conf['kafka']['consumer']['groupId']
                    topics = conf['kafka']['consumer']['topics']
            return json.dumps({groupId: ",".join(topics)})
        except:
            return "Config schema is wrong"

    def update(self, redisKey):
        p = self.redisConn.pipeline()
        appids = self.rmConn.cluster_applications(state="RUNNING", application_types=["SPARK"]).data
        appids = appids['apps']['app']
        userList = ['hive', 'hdfs', 'spark']
        for appid in appids:
            if appid['user'] not in userList:
                configPath = self.getConfPath(appid['id'], appid['trackingUrl'])
                groupAndTopics = self.getGroupIdAndTopics(configPath)
                if re.findall(r'^WIPX.*', groupAndTopics[0]) == []:
                    p.hset(redisKey, appid['name'].split(":")[0], groupAndTopics)

        p.execute()