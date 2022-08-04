import os
import time
import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn = boto3.client("stepfunctions")
SFN_ROLE = os.environ['SFN_ROLE']
SFN_ARN = os.environ['SFN_ARN']


def create_state_function(definition_str):

    definition = {
                  "Comment": "A simple states machine",
                  "StartAt": "Begin",
                  "States": {
                    "Begin": {
                      "Type": "Pass",
                      "Next": "IntegrationTest"
                    },
                    "IntegrationTest": {
                      "Type": "Map",
                      "InputPath": "$.datasetids",
                      "ItemsPath": "$.datasets",
                      "MaxConcurrency": 3,
                      "Iterator": json.loads(definition_str),
                      "End": True
                    }
                  }
                }

    response = sfn.create_state_machine(
        name="simple-state-machine",
        definition=json.dumps(definition),
        roleArn=SFN_ROLE,
        type="STANDARD"
    )
    return response


def start_state_machine(sfn_arn):
    datasetids_dict = json.load(open('datasetids.json'))

    response = sfn.start_execution(
        stateMachineArn=sfn_arn,
        input=json.dumps(datasetids_dict)
    )
    return response


def describe_sfn_execution(execution_arn):
    response = sfn.describe_execution(
        executionArn=execution_arn
    )
    return response


def handler(event, context):
    logger.info(f"Received event: {event}")

    # describe state machine
    sfn_description = sfn.describe_state_machine(
        stateMachineArn=SFN_ARN
    )

    # create state machine
    sfn_creation_response = create_state_function(sfn_description['definition'])

    # if creation is successful
    if 'stateMachineArn' in sfn_creation_response:

        try:
            # start state machine
            sfn_execution_response = start_state_machine(sfn_arn=sfn_creation_response['stateMachineArn'])

            # default execution status
            execution_status = 'RUNNING'

            # poll state machine execution to know the current execution status
            while execution_status == 'RUNNING':
                time.sleep(300)
                sfn_execution_info = describe_sfn_execution(execution_arn=sfn_execution_response['executionArn'])
                execution_status = sfn_execution_info['status']

            if execution_status != 'SUCCEEDED':
                raise Exception("Step function failed")

        except Exception as e:
            logger.error(e)

    # return sfn_description['definition']
