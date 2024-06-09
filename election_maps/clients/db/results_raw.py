from election_maps.entities.action import ObserverAction
from election_maps.clients.db.base import BaseDatabaseHandler


class RawResultsDatabaseHandler(BaseDatabaseHandler):
    def __init__(self):
        super().__init__("raw_results_collection")

    def add_one_action(self, action: ObserverAction):
        self.insert_one(action.to_dict())
