#
# Lambda function detect labels in image using Amazon Rekognition
#

from __future__ import print_function
import boto3
import json
import os
from boto3.dynamodb.conditions import Key, Attr

minCofidence = 60


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

    rekFunction(bucket, key)


def rekFunction(bucket, key):
    print("Detected the following image in S3")
    print("Bucket: " + bucket + " key name: " + key)

    client = boto3.client("rekognition")

    response = client.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}},
                                    MaxLabels=10, MinConfidence=minCofidence)

    # Get the service resource
    dynamodb = boto3.resource("dynamodb")

    # Instantiate a table resource object
    imageLabelsTable = os.environ["TABLE"]
    table = dynamodb.Table(imageLabelsTable)

    # Put item into table
    table.put_item(
        Item={"Image": key}
    )
