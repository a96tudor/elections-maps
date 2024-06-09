import datetime
from typing import Optional, List

from election_maps.types import (
    VotingSessionType, ObserverActionType, ObserverActionStatusType
)
from election_maps.entities.candidates import Candidate
from election_maps.entities.sections import VotingSection
from election_maps.clients.db.users import UsersDatabaseHandler
from election_maps.clients.db.results import ResultsDatabaseHandler
from election_maps.entities.observer import Observer


class ObserverAction:
    def __init__(
        self,
        observer_id: str,
        voting_session: VotingSessionType,
        action_type: ObserverActionType,
        entity_id: str,
        status: Optional[ObserverActionStatusType] = None,
        db_id: Optional[str] = None,
    ):
        self.observer_id = observer_id
        self.voting_session = voting_session
        self.action_type = action_type
        self.entity_id = entity_id
        self.db_id = db_id

        if status:
            self.status = status
        else:
            self.status = ObserverActionStatusType.ACKNOWLEDGED

        self.timestamp: datetime.datetime = datetime.datetime.now()

        self._observer: Observer = None
        self._voting_section: VotingSection = None

    def to_dict(self) -> dict:
        return {
            "observerId": self.observer_id,
            "votingSession": self.voting_session.value,
            "actionType": self.action_type.value,
            "status": self.status.value,
            "entity_id": self.entity_id,
            "timestamp": self.timestamp
        }

    @property
    def candidate(self) -> Candidate:
        return Candidate.from_id(self.entity_id)

    @property
    def key(self) -> (str, str, str):
        return self.observer_id, self.voting_session, self.entity_id

    @property
    def voting_section(self) -> VotingSection:
        if self._voting_section is None:
            db_handler = ResultsDatabaseHandler()
            self._voting_section = db_handler.get_voting_section_by_number(
                self.observer.voting_section_number
            )
        return self._voting_section

    @property
    def observer(self) -> Observer:
        if self._observer is None:
            self._observer = UsersDatabaseHandler().get_user_by_id(self.observer_id)

        return self._observer

    @classmethod
    def from_dict(cls, observer_action: dict) -> "ObserverAction":
        db_id = None
        if observer_action.get("_id"):
            db_id = str(observer_action.get("_id"))

        return cls(
            observer_id=observer_action["observerId"],
            voting_session=VotingSessionType(observer_action["votingSession"]),
            action_type=ObserverActionType(observer_action["actionType"]),
            status=ObserverActionStatusType(observer_action["status"]),
            entity_id=observer_action['entity_id'],
            db_id=db_id,
        )


class ObserverActionsCollection(list):
    def __init__(self):
        super().__init__()

    @property
    def grouped(self) -> dict:
        result = {}

        for action in self:
            if action.key not in result:
                result[action.key] = ObserverActionsCollection()
            result[action.key].append(action)

        return result

    @property
    def increment_count(self):
        return sum(
            action.action_type == ObserverActionType.INCREMENT for action in self
        )

    @property
    def decrement_count(self):
        return sum(
            action.action_type == ObserverActionType.DECREMENT for action in self
        )

    @property
    def voting_sections(self) -> List[VotingSection]:
        return list({action.voting_section for action in self})

    @property
    def voting_section_grouped(self) -> VotingSection:
        return self[0].voting_section
