import requests
from ratelimit import limits, sleep_and_retry


REQUESTS_PER_MINUTE = 15


class BaseRequests:

    def  __init__(self, host):
        self.host = host


    @sleep_and_retry
    @limits(calls=1, period=60/REQUESTS_PER_MINUTE)
    def __request(self, type, endpoint, **kwargs):
        url = self.host + endpoint
        if type == "post":
            return requests.post(url=url, **kwargs)
        elif type == "get":
            return requests.get(url=url, **kwargs)
        else:
            raise ValueError()


    def post(self, endpoint, **kwargs):
        return self.__request("post", endpoint, **kwargs)


    def get(self, endpoint, **kwargs):
        return self.__request("get", endpoint, **kwargs)
