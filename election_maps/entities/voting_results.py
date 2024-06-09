from typing import Optional

from election_maps.entities.candidates import Candidate
from election_maps.types import ObserverActionType


class VotingResult:
    def __init__(self, candidate: Candidate, votes: int):
        self.votes = votes
        self.candidate = candidate
        self.percentage = None

    @property
    def percentage_string(self) -> str:
        return f"{(self.percentage * 100):.2f}%"

    @property
    def name(self) -> str:
        return self.candidate.name

    @property
    def id(self) -> str:
        return self.candidate.id

    @classmethod
    def from_dict(cls, voting_result):
        return cls(
            candidate=Candidate.from_dict(voting_result["candidate"]),
            votes=voting_result["votes"],
        )

    def to_dict(self) -> dict:
        return {"candidate": self.candidate.to_dict(), "votes": self.votes}

    def process_actions(self, actions):
        decrement_actions = actions.decrement_count
        increment_actions = actions.increment_count

        self.votes += increment_actions - decrement_actions


class VotingResultCollection(list):
    def __init__(self, invalid_votes):
        super().__init__()

        self.invalid_votes = invalid_votes

    @property
    def sorted(self):
        return sorted(self, key=lambda x: -x.votes)

    def to_dict(self) -> dict:
        return {
            "valid_votes": [result.to_dict() for result in self],
            "invalid_votes": self.invalid_votes
        }

    @classmethod
    def from_dict(cls, voting_results) -> "VotingResultCollection":
        voting_result_collection = cls(voting_results["invalid_votes"])

        for valid_vote in voting_results["valid_votes"]:
            voting_result_collection.append(VotingResult.from_dict(valid_vote))

        return voting_result_collection

    def get_by_id(self, result_id: str) -> Optional[VotingResult]:
        for result in self:
            if result.id == result_id:
                return result

        return None
