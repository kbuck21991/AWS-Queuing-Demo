import boto3
import requests
import urllib

#API Constants for Keys, Domains, Endpoints
API_KEY = 'Eaw3he5JJQ9b5levIta4Hv1uX6QeKO'
API_DOMAIN = "https://www.worldcoinindex.com/apiservice"
API_ENDPOINTS = {
    "ticker" : "/ticker"
}

#API Constants for ease of creation of URL
TICKER_SYMBOLS = "ethbtc-ltcbtc-eosbtc-bchbtc-xrpbtc"
FIAT_CURRENCY = "usd"

#function to call the WCI API given variables for the endpoint and a list of parameters to pass
def getDataFromAPI(endpoint, params):
    url = API_DOMAIN + endpoint
    qs = urllib.parse.urlencode(params)
    return requests.get(url+"?"+qs).text

#create the parameters and call endpoint for ticker
def getTickerData():
    params = {
        "key": API_KEY,
        "label": TICKER_SYMBOLS,
        "fiat": FIAT_CURRENCY
    }
    return getDataFromAPI(API_ENDPOINTS["ticker"], params)

# Get the service client and resource handlers
def initAmazonHandlers():
    return boto3.client('sqs'), boto3.resource('sqs')

#lambda function for enqueing API data from World Coin Index to SQS
def enqueue_handler(event, context):
    sqsClient, sqsResource = initAmazonHandlers()

    data = getTickerData()

    # Get the queue.
    queue = sqsResource.get_queue_by_name(QueueName='WCI_CoinDataDigestQueue')

    # Send message to SQS queue
    response = sqsClient.send_message(
        QueueUrl=queue.url,
        DelaySeconds=10,
        MessageBody=(
            data
        )
    )

    return {
        'queue':queue.url,
        'messageID': response['MessageId'],
        'data': data
    }
