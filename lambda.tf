data "archive_file" "lambda_script_zip" {
  source_dir  = "${path.module}/scripts/"
  output_path = "${path.module}/scripts.zip"
  type        = "zip"
}

resource "aws_lambda_function" "test_lambda_function" {
  function_name = "test_lambda_function"
  handler       = "test_lambda.handler"
  role          = aws_iam_role.iam_role_for_test_lambda.arn
  runtime       = "python3.8"
  timeout       = 900

  filename         = data.archive_file.lambda_script_zip.output_path
  source_code_hash = data.archive_file.lambda_script_zip.output_base64sha256
  environment {
    variables = {
      SFN_ROLE = aws_iam_role.iam_role_for_simple_sfn.arn,
      SFN_ARN = aws_sfn_state_machine.simple_sfn_state_machine.arn
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.test_lambda_policy_attachment,
    aws_iam_role_policy_attachment.simple_sfn_policy_attachment,
    aws_sfn_state_machine.simple_sfn_state_machine
  ]
}

resource "aws_iam_role" "iam_role_for_test_lambda" {
  name = "iam_for_test_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "test_lambda_policy" {
  name        = "test-lambda-policy"
  description = "A test policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "${aws_iam_role.iam_role_for_simple_sfn.arn}"
    },
    {
      "Effect": "Allow",
      "Action": [
        "states:CreateStateMachine",
        "states:DescribeStateMachine",
        "states:StartExecution",
        "states:DescribeExecution"
      ],
      "Resource": "arn:aws:states:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "test_lambda_policy_attachment" {
  role       = aws_iam_role.iam_role_for_test_lambda.name
  policy_arn = aws_iam_policy.test_lambda_policy.arn
}

#resource "aws_lambda_invocation" "invoke_test_lambda" {
#  function_name = aws_lambda_function.test_lambda_function.function_name
#  input = jsonencode({
#    key1 = "value1"
#    key2 = "value2"
#  })
#}