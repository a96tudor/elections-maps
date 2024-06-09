from typing import Optional, Any
import json
from contextlib import contextmanager

import boto3
from botocore.exceptions import ClientError

from election_maps.clients.aws.constants import (
    PROFILE_NAME, DATABASE_SECRET_NAME, REGION_NAME, GENERAL_SECRET_NAME
)


class AWSSecretsConfig:
    def __init__(self, secret_string: str):
        secret_values = json.loads(secret_string)

        for key, value in secret_values.items():
            self.__setattr__(key, value)

    def __getattribute__(self, item) -> Optional[Any]:
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return None


def get_database_secrets():
    # Create a Secrets Manager client
    session = boto3.session.Session(profile_name=PROFILE_NAME)
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=DATABASE_SECRET_NAME
        )
    except ClientError as e:
        raise e

    return AWSSecretsConfig(get_secret_value_response["SecretString"])


def get_whatsapp_link() -> str:
    session = boto3.session.Session(profile_name=PROFILE_NAME)
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=GENERAL_SECRET_NAME
        )
    except ClientError as e:
        raise e

    return AWSSecretsConfig(get_secret_value_response["SecretString"]).whatsapp_link

