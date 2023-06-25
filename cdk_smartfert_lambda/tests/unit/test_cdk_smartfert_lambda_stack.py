import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_smartfert_lambda.cdk_smartfert_lambda_stack import CdkSmartfertLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_smartfert_lambda/cdk_smartfert_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkSmartfertLambdaStack(app, "cdk-smartfert-lambda")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
