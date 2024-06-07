class MayorCandidate:
    def __init__(self, name: str, party: str):
        self.name = name
        self.party = party

    @classmethod
    def from_dict_csv(cls, candidate: dict) -> "MayorCandidate":
        return cls(candidate['Nume'], candidate['Partid'])

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
