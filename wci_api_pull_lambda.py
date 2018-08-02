import boto3
import requests

#lambda function for enqueing API data from World Coin Index to SQS
def enqueue_handler(event, context):
    # Get the service resource
    sqsClient = boto3.client('sqs')
    sqsResource = boto3.resource('sqs')

    # Get the queue.
    queue = sqsResource.get_queue_by_name(QueueName='WCI_CoinDataDigestQueue')

    # Send message to SQS queue
    response = sqsClient.send_message(
        QueueUrl=queue.url,
        DelaySeconds=10,
        MessageBody=(
            'Test Message to send to SQS'
        )
    )

    return {
        'queue':queue.url,
        'messageID': response['MessageId']
    }
