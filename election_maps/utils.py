from flask import Flask

LOCAL_URL = 'http://127.0.0.1:8000'
SERVER_URL = ''  # TODO: Fill this in once we know where we deploy


def get_api_url(app: Flask) -> str:
    if app.debug:
        return LOCAL_URL
    return SERVER_URL
