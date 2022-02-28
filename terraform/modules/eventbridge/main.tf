resource "aws_cloudwatch_event_rule" "cloudwatch_event_rule" {
  name = "capture-event-for-lambda"
  description = "Capture event to trigger lambda function"

  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule = aws_cloudwatch_event_rule.cloudwatch_event_rule.name
  target_id = "SendToLambda"
  arn  = var.lambda_arn
}

resource "aws_lambda_permission" "allow_event_trigger_trigger" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.cloudwatch_event_rule.arn
}