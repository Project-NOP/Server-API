import boto3

from app.constants.aws.vpc import SSM_VPCE_URL

ssm = boto3.client("ssm", endpoint_url=SSM_VPCE_URL)
