from election_maps.entities.voting_results import VotingResultCollection


class VotingSection:
    def __init__(
        self, number, name, searchable_name, latitude=None, longitude=None,
        mayor_results=None, local_council_results=None,
        county_council_president_results=None,
        county_council_results=None, db_id=None,
    ):
        self.number = number
        self.name = name
        self.searchable_name = searchable_name
        self.latitude = latitude
        self.longitude = longitude

        self.mayor_results = mayor_results
        self.local_council_results = local_council_results
        self.county_council_president_results = county_council_president_results
        self.county_council_results = county_council_results

        self.db_id = db_id

    @classmethod
    def from_dict(cls, voting_section) -> "VotingSection":
        db_id = None
        if voting_section.get("_id"):
            db_id = str(voting_section.get("_id"))

        return cls(
            voting_section["number"],
            voting_section["name"],
            voting_section["searchable_name"],
            voting_section["latitude"],
            voting_section["longitude"],
            VotingResultCollection.from_dict(voting_section["results"]["mayor"]),
            VotingResultCollection.from_dict(
                voting_section["results"]["local_council"],
            ),
            VotingResultCollection.from_dict(
                voting_section["results"]["county_council_president"],
            ),
            VotingResultCollection.from_dict(
                voting_section["results"]["county_council"],
            ),
            db_id=db_id,
        )

    @classmethod
    def from_dict_thin(cls, voting_section) -> "VotingSection":
        return cls(
            voting_section["number"],
            voting_section["name"],
            voting_section["searchable_name"],
            voting_section["latitude"],
            voting_section["longitude"],
        )

    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "name": self.name,
            "searchable_name": self.searchable_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "results": {
                "mayor": self.mayor_results.to_dict(),
                "local_council": self.local_council_results.to_dict(),
                "county_council_president": (
                    self.county_council_president_results.to_dict()
                ),
                "county_council": self.county_council_results.to_dict()
            }
        }


class VotingSectionsCollection(list):
    def __init__(self):
        super().__init__()

        self._by_number = {}

    def append(self, voting_section):
        super().append(voting_section)

        self._by_number[voting_section.number] = voting_section

    def get(self, number):
        return self._by_number[number]
