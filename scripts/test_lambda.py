import os
import time
import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn = boto3.client("stepfunctions")
sfn_role = os.environ['SFN_ROLE']
sfn_arn = os.environ['SFN_ARN']


def create_state_function():
    sfn_json_dict = json.load(open('step_function.json'))
    logger.info("We are herey")
    logger.info(sfn_json_dict)

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
                      "Iterator": sfn_json_dict,
                      "End": True
                    }
                  }
                }

    logger.info(definition)
    logger.info("the json string version")
    logger.info(json.dumps(definition))

    response = sfn.create_state_machine(
        name="simple-state-machine",
        definition=json.dumps(definition),
        roleArn=sfn_role,
        type="STANDARD"
    )
    return response


def start_state_machine(sfn_arn):
    response = sfn.start_execution(
        stateMachineArn=sfn_arn,
        input="{\"first_name\" : \"test\"}"
    )
    return response


def describe_sfn_execution(execution_arn):
    response = sfn.describe_execution(
        executionArn=execution_arn
    )
    return response


def handler(event, context):
    logger.info(f"Received event: {event}")

    # sfn_json_dict = json.load(open('step_function.json'))
    # sfn_definition = json.dumps(sfn_json_file)

    # logger.info(sfn_json_dict)

    # describe state machine
    # sfn_description = sfn.describe_state_machine(
    #     stateMachineArn=sfn_arn
    # )

    # create state machine
    sfn_creation_response = create_state_function()

    # # if creation is successful
    # if 'stateMachineArn' in sfn_creation_response:
    #
    #     # start state machine
    #     sfn_execution_response = start_state_machine(sfn_arn=sfn_creation_response['stateMachineArn'])
    #
    #     # default execution status
    #     execution_status = 'RUNNING'
    #
    #     # poll state machine execution to know the current execution status
    #     while execution_status == 'RUNNING':
    #         time.sleep(5)
    #         sfn_execution_info = describe_sfn_execution(execution_arn=sfn_execution_response['executionArn'])
    #         execution_status = sfn_execution_info['status']
    #
    #     if execution_status != 'SUCCEEDED':
    #         raise Exception("Step function failed")
    #
    #     logger.info(sfn_execution_info)
    # logger.info(sfn_description)

    # return sfn_description['definition']
