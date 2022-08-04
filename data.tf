data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "lambda_script_zip" {
  source_dir  = "${path.module}/scripts/"
  output_path = "${path.module}/scripts.zip"
  type        = "zip"
}

data "template_file" "sfn_definition" {
  template = file("scripts/step_function.json")
  vars = {
    lambda_arn = aws_lambda_function.convert_to_number_lambda_function.arn
  }
}