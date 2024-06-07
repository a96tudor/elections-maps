from pyutils.database.mongo.client_handler import MongoClientHandler

from election_maps.clients.aws.config import get_database_secrets


def _get_aws_config(collection_secret_name: str) -> dict:
    db_secret = get_database_secrets()

    connection_string = (
        f"mongodb+srv://{db_secret.username}:{db_secret.password}@{db_secret.url}"
    )
    return {
        "connection_string": connection_string,
        "database_name": db_secret.database_name,
        "collection_name": db_secret.__getattribute__(collection_secret_name),
    }


class BaseDatabaseHandler(MongoClientHandler):
    def __init__(self, collection_secret_name: str):
        super().__init__(**_get_aws_config(collection_secret_name))
