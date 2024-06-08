from election_maps.clients.db.base import BaseDatabaseHandler
from election_maps.entities.observer import Observer


class UsersDatabaseHandler(BaseDatabaseHandler):
    def __init__(self):
        super().__init__("users_collection")

    def add_users(self, users: [Observer]) -> [str]:
        return self.insert_batch([user.to_dict() for user in users])
