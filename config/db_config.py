from config import ssm


class LocalDBConfig:
    MONGODB_SETTINGS = {"host": "localhost", "port": 27017, "db": "nop"}


class RemoteDBConfig:
    host, port, db = ssm.get_parameter(Name="nop-mongodb-connection-info")["Parameter"][
        "Value"
    ].split(",")

    MONGODB_SETTINGS = {"host": host, "port": int(port), "db": db}
