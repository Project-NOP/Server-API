import boto3

ssm = boto3.client(
    "ssm",
    endpoint_url="https://vpce-091e176e927058503-ububuzil.ssm.ap-northeast-2.vpce.amazonaws.com",
)
