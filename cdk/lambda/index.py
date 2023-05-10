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