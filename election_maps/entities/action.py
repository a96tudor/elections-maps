import datetime
from typing import Optional

from election_maps.types import (
    VotingSessionType, ObserverActionType, ObserverActionStatusType
)


class ObserverAction:
    def __init__(
        self,
        observer_id: str,
        voting_session: VotingSessionType,
        action_type: ObserverActionType,
        entity_id: str,
        status: Optional[ObserverActionStatusType] = None
    ):
        self.observer_id = observer_id
        self.voting_session = voting_session
        self.action_type = action_type
        self.entity_id = entity_id

        if status:
            self.status = status
        else:
            self.status = ObserverActionStatusType.ACKNOWLEDGED

        self.timestamp: datetime.datetime = datetime.datetime.now()

        self._observer = None

    def to_dict(self) -> dict:
        return {
            "observerId": self.observer_id,
            "votingSession": self.voting_session.value,
            "actionType": self.action_type.value,
            "status": self.status.value,
            "entity_id": self.entity_id,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, observer_action: dict) -> "ObserverAction":
        return cls(
            observer_id=observer_action["observerId"],
            voting_session=VotingSessionType(observer_action["votingSession"]),
            action_type=ObserverActionType(observer_action["actionType"]),
            status=ObserverActionStatusType(observer_action["status"])
        )
