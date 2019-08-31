from config import ssm


class LocalLevelConfig:
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "85c145a16bd6f6e1f3e104ca78c6a102"


class ProductionLevelConfig:
    ENV = "production"
    DEBUG = False
    SECRET_KEY = ssm.get_parameter(Name="nop-was-secret-key")["Parameter"]["Value"]
