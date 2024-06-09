from election_maps.entities.action import ObserverAction, ObserverActionsCollection
from election_maps.clients.db.base import BaseDatabaseHandler
from election_maps.types import ObserverActionStatusType


class RawResultsDatabaseHandler(BaseDatabaseHandler):
    def __init__(self):
        super().__init__("raw_results_collection")

    def add_one_action(self, action: ObserverAction):
        self.insert_one(action.to_dict())

    def get_acknowledged_actions(self) -> ObserverActionsCollection:
        result = ObserverActionsCollection()

        cursor = self.find_many(
            query={"status": ObserverActionStatusType.ACKNOWLEDGED.value}
        )

        for action in cursor:
            result.append(ObserverAction.from_dict(action))

        return result

    def get_acknowledged_actions_for_observer(
        self, observer_id: str
    ) -> ObserverActionsCollection:
        result = ObserverActionsCollection()

        cursor = self.find_many(
            query={
                "status": ObserverActionStatusType.ACKNOWLEDGED.value,
                "observerId": observer_id,
            }
        )

        for action in cursor:
            result.append(ObserverAction.from_dict(action))

        return result

    def batch_update_status(self, ids: [str], new_status: ObserverActionStatusType):
        action_ids = [self.id_from_string(id) for id in ids]

        query = {"field": {"$in": action_ids}}

        self.update_all(query, {"status": new_status.value})
