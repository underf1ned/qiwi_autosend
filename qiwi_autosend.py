import requests
import time
import json
import config

def sendRequest(pr, url, token, params = {}):
    s = requests.Session()
    s.headers["Content-Type"] = "application/json"
    s.headers["Accept"] = "application/json"
    s.headers["Authorization"] = "Bearer " + token
    
    response = s.post(pr + "://edge.qiwi.com" + url, json = params)
    return json.loads(response.text)

def transferBalance(token, amount):
    params = {
        "id": str(int(time.time() * 1000)),
        "sum": {
            "amount": amount,
            "currency": "643"
            },
        "paymentMethod": {
            "type": "Account",
            "accountId": "643"
            },
        "fields": {
            "account": config.qiwi_number
            }
        }
    sendRequest("https", "/sinap/api/v2/terms/99/payments", token, params)

def getBalance(token):
    response = sendRequest("http", "/funding-sources/v1/accounts/current", token)
    return response["accounts"][0]["balance"]["amount"]

while True:
    for qiwi_token in config.qiwi_tokens:
        balance = getBalance(qiwi_token)
        if balance > 0:
            transferBalance(qiwi_token, balance)
    time.sleep(config.interval)
