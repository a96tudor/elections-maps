import abc
from typing import Optional


class Candidate:
    def __init__(self, name: str):
        self.name = name

        self.id = None

    @classmethod
    def from_dict(cls, candidate: dict) -> "Candidate":
        if candidate.get("firstName") and candidate.get("lastName"):
            return IndividualCandidate.from_dict(candidate)
        return CouncilCandidate.from_dict(candidate)

    @classmethod
    def from_dict_csv(cls, candidate: dict) -> "Candidate":
        if candidate.get("Nume") and candidate.get("Prenume"):
            return IndividualCandidate.from_dict_csv(candidate)
        return CouncilCandidate.from_dict_csv(candidate)

    @abc.abstractmethod
    def to_dict(self) -> dict:
        ...


class IndividualCandidate(Candidate):
    def __init__(self, first_name: str, last_name: str, party: str):
        super().__init__(f"{last_name}, {first_name}")
        self.first_name = first_name
        self.last_name = last_name
        self.party = party
        self.id = f"{self.first_name}.{self.last_name}.{self.party.replace(' ', '')}"

    @classmethod
    def from_dict_csv(cls, candidate: dict) -> "IndividualCandidate":
        return cls(
            candidate['Prenume'], candidate['Nume'], candidate['Partid']
        )

    @classmethod
    def from_dict(cls, candidate: dict) -> "IndividualCandidate":
        return cls(candidate["firstName"], candidate["lastName"], candidate["party"])

    def to_dict(self) -> dict:
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "name": self.name,
            "party": self.party
        }


class CouncilCandidate(Candidate):
    def __init__(self, party: Optional[str] = None, name: Optional[str] = None):
        super().__init__(party if party else name)

        if name is None and party is None:
            raise Exception("At least one of name and party should be provided")

        self.id = self.name

    @classmethod
    def from_dict_csv(cls, candidate: dict) -> "CouncilCandidate":
        return cls(candidate.get('Partid'), candidate.get('Nume'))

    @classmethod
    def from_dict(cls, candidate: dict) -> "CouncilCandidate":
        return cls(name=candidate.get("name"))

    def to_dict(self) -> dict:
        return {"name": self.name}


class Candidates(list):
    def __init__(self):
        super().__init__()
        self._by_name = {}

    def append(self, candidate):
        super().append(candidate)
        self._by_name[candidate.name] = candidate

    def get_by_name(self, name):
        return self._by_name[name]

    def to_dicts(self) -> [dict]:
        return [candidate.to_dict() for candidate in self]
