import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn = boto3.client("stepfunctions")
sfn_role = os.environ['SFN_ROLE']


def create_state_function():
    response = sfn.create_state_machine(
        name="simple-state-machine",
        definition="""
            {
              "Comment": "A simple states machine",
              "StartAt": "HelloWorld",
              "States": {
                "HelloWorld": {
                  "Type": "Pass",
                  "End": true
                }
              }
            }
        """,
        roleArn=sfn_role,
        type="STANDARD"
    )
    return response


def handler(event, context):
    logger.info(f"Received event")
    sfn_creation_response = create_state_function()

    return sfn_creation_response
