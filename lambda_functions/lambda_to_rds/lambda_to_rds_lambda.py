import boto3
import sys
import rds_config
import pymysql
from decimal import Decimal
import logging

#initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Get DB variables from configFile
rds_host  = rds_config.rds_host
rds_username = rds_config.db_username
rds_password = rds_config.db_password
rds_db_name = rds_config.db_name

#Create Database connection and log errors if needed. Per AWS docs, do this outside of the event handler for performance reasons.
try:
    conn = pymysql.connect(rds_host, user=rds_username, passwd=rds_password, db=rds_db_name, connect_timeout=5)
    logger.info("Connection Established")
except Exception as e:
    logger.info("Error Establishing Connection to Database. Error Details => " + repr(e))
    sys.exit()

#lambda function for inserting Data into the MySQL DB from Lambda
def lambda_to_rds_handler(event, context):

    #Insert Data from the passed Lambda Event into the MySQL DB
    with conn.cursor() as cur:
        for coin in event["Markets"]:
            cur.execute('insert into wci_coindata (Label, Name, Price, Volume, Timestamp) values("'+coin["Label"]+'","'+coin["Name"]+'", "'+str(Decimal(coin["Price"]))+'", "'+str(Decimal(coin["Volume_24h"]))+'", "'+str(coin["Timestamp"])+'") ')
        conn.commit()

    logger.info("Inserted New Coin Data to RDS Successfully.")
