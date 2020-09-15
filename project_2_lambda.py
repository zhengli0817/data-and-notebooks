
import csv
import uuid
import json 
import sys 
from datetime import datetime
# -- update Boto3 to latest -- 
from pip._internal import main

main(['install', 'boto3', '--target', '/tmp/'])
sys.path.insert(0,'/tmp/')
import boto3
from botocore.exceptions import ClientError
from pip._internal import main


# -- make a connection to fraud detector -- 
client = boto3.client("frauddetector")

# -- specify defaults: entity, detector and model  -- 
ENTITY_TYPE   = "customer"
EVENT_TYPE    = "account_registration" 
DETECTOR_NAME = "project_1_detector"
DETECTOR_VER  = "1"
MODEL_NAME    = "project_1_model"
MODEL_VER     = "1.0"


def lambda_handler(event, context):
    eventId     = uuid.uuid1()
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        pred = client.get_event_prediction(detectorId    = DETECTOR_NAME, 
                                       detectorVersionId = DETECTOR_VER,
                                       eventId           = str(eventId),
                                       eventTypeName     = EVENT_TYPE,
                                       eventTimestamp    = timestampStr, 
                                       entities          = [{'entityType': ENTITY_TYPE, 'entityId':str(eventId.int)}],
                                       eventVariables    =  event) 
                                       
        event['prediction_id']    = str(eventId)
        event["detector_score"]   = pred['modelScores'][0]['scores']["{0}_insightscore".format(MODEL_NAME)]
        event["detector_outcome"] = pred['ruleResults'][0]['outcomes']
        return {
            'statusCode': 200,
            'body': event
        } 
    except:
        event['prediction_id']    = str(eventId)
        event["detector_score"]   = "-999"
        event["detector_outcome"] = "error"
        return {
            'statusCode': 200,
            'body': event
        } 
    