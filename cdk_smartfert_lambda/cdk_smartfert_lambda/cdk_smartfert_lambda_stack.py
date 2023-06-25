import os
from aws_cdk import (
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)
from aws_cdk.core import Stack, Construct, Duration


class CdkSmartfertLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        smart_fert_handler = _lambda.Function(
            self,
            'SmartFertHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.asset('./lambda-package.zip'),  # get from environment variable
            handler='handler.lambda_handler',
            environment={
                "ENV": "prod"
            },
            timeout=Duration.seconds(15),
        )

        vpc = ec2.Vpc(self, "SmartFertLambdaVpc", max_azs=2)

        database = rds.DatabaseInstance(
            self,
            "SmartFertLambdaDatabase",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_13),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            vpc=vpc,
            multi_az=True,
            allocated_storage=20,
            database_name="smartfert",
            credentials=rds.Credentials.from_password(
                "database-username",
                secretsmanager.Secret.from_secret_arn(self, "password-secret-arn", "password-secret-arn")
            )
        )

        apigw.LambdaRestApi(
            self,
            "smart_fert_api",
            rest_api_name='smart_fert_api',
            handler=smart_fert_handler,
            proxy=True
        )

        smart_fert_handler.add_to_role_policy(
            iam.PolicyStatement(
                actions=["rds-db:connect"],
                resources=[database.secret.secret_arn]
            )
        )
