const cdk = require("@aws-cdk/core");
const s3 = require("@aws-cdk/aws-s3");
const iam = require("@aws-cdk/aws-iam");
const lambda = require("@aws-cdk/aws-lambda");
const lambdaEventSource = require("@aws-cdk/aws-lambda-event-sources");
const dynamodb = require("@aws-cdk/aws-dynamodb");

const imageBucket = "cdk-rekn-imagebucket";

class CdkAppStack extends cdk.Stack {
    /**
     *