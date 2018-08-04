import boto3
import sys
import rds_config
import pymysql

rds_host  = "hddbmysql01.cls0ucqv4nms.us-east-2.rds.amazonaws.com"
rds_username = rds_config.db_username
rds_password = rds_config.db_password
rds_db_name = rds_config.db_name

# Get the service client and resource handlers
def initAmazonHandlers():
    return boto3.client('sqs'), boto3.resource('sqs')

def initConnection():
    try:
        return pymysql.connect(rds_host, user=rds_username, passwd=rds_password, db=rds_db_name, connect_timeout=5)
    except:
        sys.exit()

#lambda function for pulling from SQS and putting the data into RDS
def sqs_to_rds_handler(event, context):
    sqsClient, sqsResource = initAmazonHandlers()

    conn = initConnection()

    # Get the queue.
    queue = sqsResource.get_queue_by_name(QueueName='WCI_CoinDataDigestQueue')



    return {
        'queue':queue.url
    }
