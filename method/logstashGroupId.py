import re, json
from utils.apiParser import apiParser
from .groupIdUpdater import groupIdUpdater

class logstashGroupId(groupIdUpdater):
    def __init__(self, redisConn):
        super().__init__(redisConn)
        self.parserConf = "parser.conf"
        self.inputConf = "000-input.conf"
        self.logstashGitUrl = "https://gitlabhost/api/v4/projects/195/repository"
        self.header = {'PRIVATE-TOKEN': 'token'}

    def getGroupIdAndTopics(self, url):
        configBody = apiParser().getRestAPI(url, header=self.header)
        groupId = re.findall(r'group_id.*', configBody)[0].split("=>")[1][2:-1]
        topics = re.findall(r'topics.*', configBody)[0].split("=>")[1]
        return json.dumps({groupId: ",".join(json.loads(topics))})

    def update(self, redisKey):
        p = self.redisConn.pipeline()
        url = r'{}/branches?per_page=100'.format(self.logstashGitUrl)
        branches = apiParser().getRestAPIToJson(url, header=self.header)
        for branch_dict in branches:
            branch = branch_dict['name']
            if branch != "master":
                url = r'{}/tree?path=config-prod&ref={}'.format(self.logstashGitUrl, branch)
                if apiParser().getRestAPI(url, header=self.header).count(r'"name":"%s"' % self.parserConf) == 1:
                    url = r'{}/files/config-prod%2F{}/raw?ref={}'.format(self.logstashGitUrl, self.parserConf, branch)
                    groupAndTopics = self.getGroupIdAndTopics(url)
                    p.hset(redisKey, branch, groupAndTopics)
                else:
                    url = r'{}/files/config-prod%2F{}/raw?ref={}'.format(self.logstashGitUrl, self.inputConf, branch)
                    groupAndTopics = self.getGroupIdAndTopics(url)
                    p.hset(redisKey, branch, groupAndTopics)

        p.execute()