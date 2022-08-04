import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn = boto3.client("stepfunctions")


def handler(event, context):
    logger.info(f"Received event: {event}")

    number = int(event)
    # execution_status = sfn_execution_info['status']

    # logger.info(json.dumps(sfn_execution_info))

    return number
