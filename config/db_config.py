from config import ssm


class LocalDBConfig:
    WRITE_DB_URL = "mysql+pymysql://root:password@127.0.0.1:3306/nop?charset=utf8mb4"


class RemoteDBConfig:
    WRITE_DB_URL = ssm.get_parameter(Name="nop-mysql-connection-string")["Parameter"][
        "Value"
    ]
