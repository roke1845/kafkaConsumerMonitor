import json
from .groupIdUpdater import groupIdUpdater

class fileGroupId(groupIdUpdater):
    def getGroupIdAndTopics(self, filename):
        return open(filename, "r").read()

    def update(self, redisKey, filePath):
        mapping = self.getGroupIdAndTopics(filePath)
        p = self.redisConn.pipeline()
        for key, groupAndTopics in json.loads(mapping).items():
            groupAndTopics = json.dumps(groupAndTopics)
            p.hset(redisKey, key, groupAndTopics)

        p.execute()
