import boto3
import json

# Get the service client and resource handlers
def initAmazonHandlers():
    return boto3.client('sqs'), boto3.resource('sqs'), boto3.client('lambda')

#lambda function for enqueing API data from World Coin Index to SQS
def sqs_to_lambda_handler(event, context):
    sqsClient, sqsResource, lambda_client = initAmazonHandlers()

    # Get the queue.
    queue = sqsResource.get_queue_by_name(QueueName='WCI_CoinDataDigestQueue')

    # Receive message from SQS queue
    response = sqsClient.receive_message(
        QueueUrl=queue.url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    message = response['Messages'][0]
    handle = message['ReceiptHandle']

    # Delete received message from queue
    sqsClient.delete_message(
        QueueUrl=queue.url,
        ReceiptHandle=handle
    )

    lambda_client.invoke(FunctionName="lambda_to_rds",
                                               InvocationType='Event',
                                               Payload=json.dumps(message['Body']))

    return {
        'msg':message['Body']
    }
