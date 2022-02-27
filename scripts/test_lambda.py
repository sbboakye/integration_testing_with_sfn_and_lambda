import os
import time
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
              "StartAt": "Hello",
              "States": {
                "Hello": {
                  "Type": "Pass",
                  "Next": "Wait Sixty Seconds"
                },
                "Wait Sixty Seconds": {
                  "Type": "Wait",
                  "Seconds": 60,
                  "Next": "Final"
                },
                "Final": {
                  "Type": "Pass",
                  "Result": "This totally works",
                  "Next": "SuccessState"
                },
                "SuccessState": {
                  "Type": "Succeed"
                }
              }
            }
        """,
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
    logger.info(f"Received event")

    # create state machine
    sfn_creation_response = create_state_function()

    # if creation is successful
    if 'stateMachineArn' in sfn_creation_response:

        # start state machine
        sfn_execution_response = start_state_machine(sfn_arn=sfn_creation_response['stateMachineArn'])

        # default execution status
        execution_status = 'RUNNING'

        # poll state machine execution to know the current execution status
        while execution_status == 'RUNNING':
            time.sleep(5)
            sfn_execution_info = describe_sfn_execution(execution_arn=sfn_execution_response['executionArn'])
            execution_status = sfn_execution_info['status']

        logger.info(sfn_execution_info)

    return None
