import requests, json
errorMessage = "Schema is not JSON"
class apiParser:
    def getRestAPIToJson(selt, url, header=None):
        try:
            requests.packages.urllib3.disable_warnings()
            re = requests.get(url, headers=header, verify=False)
            return json.loads(re.text)
        except:
            return errorMessage

    def getRestAPI(self, url, header=None):
        try:
            requests.packages.urllib3.disable_warnings()
            re = requests.get(url, headers=header, verify=False)
            return re.text
        except:
            return errorMessage