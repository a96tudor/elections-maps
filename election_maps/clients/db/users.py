from typing import Optional

from election_maps.clients.db.base import BaseDatabaseHandler
from election_maps.entities.observer import Observer


class UsersDatabaseHandler(BaseDatabaseHandler):
    def __init__(self):
        super().__init__("users_collection")

    def add_users(self, users: [Observer]) -> [str]:
        return self.insert_batch([user.to_dict() for user in users])

    def get_user_by_phone_number(self, phone_number: str) -> Optional[Observer]:
        query = {"phoneNumber": phone_number}
        cursor = self.find_one(query)

        if cursor:
            return Observer.from_dict(cursor)

        return None

    def get_user_by_id(self, user_id: str) -> Optional[Observer]:
        query = {"_id": user_id}

        cursor = self.find_one(query)

        if cursor:
            return Observer.from_dict(cursor)

        return None
