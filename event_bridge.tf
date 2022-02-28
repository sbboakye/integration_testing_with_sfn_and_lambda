#module "custom_eventbridge" {
#  source               = "./terraform/modules/eventbridge"
#  lambda_arn           = aws_lambda_function.test_lambda_function.arn
#  lambda_function_name = aws_lambda_function.test_lambda_function.function_name
#}
