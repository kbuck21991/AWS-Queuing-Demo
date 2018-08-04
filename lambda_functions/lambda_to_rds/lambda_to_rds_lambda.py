import boto3
import sys
import rds_config
import pymysql
from decimal import Decimal

rds_host  = "hddbmysql01.cls0ucqv4nms.us-east-2.rds.amazonaws.com"
rds_username = rds_config.db_username
rds_password = rds_config.db_password
rds_db_name = rds_config.db_name



try:
    conn = pymysql.connect(rds_host, user=rds_username, passwd=rds_password, db=rds_db_name, connect_timeout=5)
except:
    sys.exit()

#lambda function for enqueing API data from World Coin Index to SQS
def lambda_to_rds_handler(event, context):

    with conn.cursor() as cur:
        for coin in event["Markets"]:
            cur.execute('insert into wci_coindata (Label, Name, Price, Volume, Timestamp) values("'+coin["Label"]+'","'+coin["Name"]+'", "'+str(Decimal(coin["Price"]))+'", "'+str(Decimal(coin["Volume_24h"]))+'", "'+str(coin["Timestamp"])+'") ')
        conn.commit()


    return {
        'msg':event
    }
