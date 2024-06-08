class VotingResult:
    def __init__(self, votes):
        self.votes = votes
        self.percentage = None

    @property
    def percentage_string(self):
        return f"{(self.percentage * 100):.2f}%"


class MayorVotingResult(VotingResult):
    def __init__(self, candidate, votes):
        super().__init__(votes)
        self.candidate = candidate

    def to_dict(self):
        return {
            'candidate': self.candidate,
            'party': self.candidate.party,
            'votes': self.votes,
            'percentage': self.percentage
        }


class LocalCouncilVotingResult(VotingResult):
    def __init__(self, party, votes):
        super().__init__(votes)
        self.party = party


class VotingResultCollection(list):
    def __init__(self, valid_votes, invalid_votes):
        super().__init__()

        self.valid_votes = valid_votes
        self.invalid_votes = invalid_votes

    @property
    def sorted(self):
        return sorted(self, key=lambda x: -x.votes)

    def to_dicts(self) -> [dict]:
        return [result.to_dict() for result in self]
