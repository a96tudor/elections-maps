from election_maps.clients.db.base import BaseDatabaseHandler
from election_maps.entities.sections import VotingSection


class ResultsDatabaseHandler(BaseDatabaseHandler):
    def __init__(self):
        super().__init__("results_collection")

    def get_voting_section_by_number(self, number: str) -> VotingSection:
        query = {"number": number}

        cursor = self.find_one(query)

        return VotingSection.from_dict(cursor)
