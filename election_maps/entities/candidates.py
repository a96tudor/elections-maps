class MayorCandidate:
    def __init__(self, first_name: str, last_name: str, party: str):
        self.first_name = first_name
        self.last_name = last_name
        self.name = f"{self.last_name}, {self.first_name}"
        self.party = party
        self.id = f"{self.first_name}.{self.last_name}.{self.party.replace(' ', '')}"

    @classmethod
    def from_dict_csv(cls, candidate: dict) -> "MayorCandidate":
        return cls(
            candidate['Prenume'], candidate['Nume'], candidate['Partid']
        )

    @classmethod
    def from_dict(cls, candidate: dict) -> "MayorCandidate":
        return cls(candidate["name"], candidate["party"])

    def to_dict(self) -> dict:
        return {"name": self.name, "party": self.party}


class MayorCandidates(list):
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
