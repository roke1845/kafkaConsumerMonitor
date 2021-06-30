
class groupIdUpdater:
    def __init__(self, redisConn, rmConn=None, HDFSConn=None):
        self.HDFSConn = HDFSConn
        self.redisConn = redisConn
        self.rmConn = rmConn

    def getGroupIdAndTopics(self, *args):
        pass

    def update(self, redisKey, *args):
        pass