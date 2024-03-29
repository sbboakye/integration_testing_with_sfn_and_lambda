import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn = boto3.client("stepfunctions")


def describe_sfn_execution(execution_arn):
    response = sfn.describe_execution(
        executionArn=execution_arn
    )
    return response


def handler(event, context):
    logger.info(f"Received event: {event}")

    sfn_execution_info = describe_sfn_execution(execution_arn=event['executionArn'])
    # execution_status = sfn_execution_info['status']

    # logger.info(json.dumps(sfn_execution_info))

    return json.loads(json.dumps(sfn_execution_info, default=str))
