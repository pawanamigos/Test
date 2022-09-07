import os
from os import environ

from chalice.app import CognitoUserPoolAuthorizer

os.environ["COGNITO_POOL_ARN"] = "COGNITO_POOL_ARN"


cognito_authorizer = CognitoUserPoolAuthorizer(
    "CognitoAuthorizer",
    provider_arns=[os.getenv("COGNITO_POOL_ARN")],
)
