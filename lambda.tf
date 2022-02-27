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

  filename         = data.archive_file.lambda_script_zip.output_path
  source_code_hash = data.archive_file.lambda_script_zip.output_base64sha256
}

resource "aws_iam_role" "iam_role_for_test_lambda" {
  name = "iam_for_dummy_lambda"

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
  name        = "lambda-partiql-policy"
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
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "simple_sfn_policy_attachment" {
  role       = aws_iam_role.iam_role_for_test_lambda.name
  policy_arn = aws_iam_policy.test_lambda_policy.arn
}
