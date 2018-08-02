#coding=utf-8
from myapp_baidu.main.datasourceservice.apisdk.ApiSDKJsonClient import *


class sms_service_AccountService(ApiSDKJsonClient):

	def __init__(self, username, password, token):
		ApiSDKJsonClient.__init__(self, 'AccountService', username, password, token)

	def getAccountInfo(self, getAccountInfoRequest=None):
		return self.execute('getAccountInfo', getAccountInfoRequest)

	def updateAccountInfo(self, updateAccountInfoRequest=None):
		return self.execute('updateAccountInfo', updateAccountInfoRequest)





if __name__=='__main__':
    username = 'baidu-罗技2113872'
    password = 'Bcda1234'
    token = '3ac60d07196b5196c2617cc8c6243140'
    test = sms_service_AccountService(username, password, token)
    getAccountInfoRequest = {
            "accountFields": ["userId","cost","balance"]
            }
    res = test.getAccountInfo(getAccountInfoRequest)
    print(res)



