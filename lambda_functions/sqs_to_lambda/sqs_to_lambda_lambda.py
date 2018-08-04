import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get the service client and resource handlers
def initAmazonHandlers():
    return boto3.client('sqs'), boto3.resource('sqs'), boto3.client('lambda')

#lambda function for enqueing API data from World Coin Index to SQS
def sqs_to_lambda_handler(event, context):
    sqsClient, sqsResource, lambda_client = initAmazonHandlers()

    logger.info("Event Details => " + str(event))

    # Get the queue.
    queue = sqsResource.get_queue_by_name(QueueName='WCI_CoinDataDigestQueue')
    logger.info("SQS URL => " + queue.url)

    #Grab the data from the SQS Event that is auto-triggering the Lambda
    message = event['Records'][0]
    handle = message['receiptHandle']
    logger.info("Message Details => " + str(message))

    # Delete received message from queue
    sqsClient.delete_message(
        QueueUrl=queue.url,
        ReceiptHandle=handle
    )

    #Invoke Passthrough Lambda due to VPC issues.
    lambda_client.invoke(FunctionName="lambda_to_rds",
                                               InvocationType='Event',
                                               Payload=message['body'])
