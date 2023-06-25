#!/usr/bin/env python3
import os

from aws_cdk import core

from cdk_smartfert_lambda.cdk_smartfert_lambda_stack import CdkSmartfertLambdaStack

app = core.App()
CdkSmartfertLambdaStack(app, "CdkSmartfertLambdaStack",
                        )

app.synth()
