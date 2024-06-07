class VotingInformation:
    def __init__(
            self,
            total_possible_voters,
            total_voters,
            men_18_24,
            men_25_34,
            men_35_44,
            men_45_64,
            men_65_over,
            women_18_24,
            women_25_34,
            women_35_44,
            women_45_64,
            women_65_over,
    ):
        self.total_possible_voters = total_possible_voters
        self.total_voters = total_voters

        self.men_18_24 = men_18_24
        self.men_25_34 = men_25_34
        self.men_35_44 = men_35_44
        self.men_45_64 = men_45_64
        self.men_65_over = men_65_over

        self.women_18_24 = women_18_24
        self.women_25_34 = women_25_34
        self.women_35_44 = women_35_44
        self.women_45_64 = women_45_64
        self.women_65_over = women_65_over

    @property
    def attendance(self):
        return self.total_voters / self.total_possible_voters

    @property
    def attendance_percentage(self):
        return f"{(self.attendance * 100):.2f}%"

    @property
    def total_men(self):
        return (
            self.men_18_24 + self.men_25_34 + self.men_35_44 +
            self.men_45_64 + self.men_65_over
        )

    @property
    def total_women(self):
        return (
            self.women_18_24 + self.women_25_34 + self.women_35_44 +
            self.women_45_64 + self.women_65_over
        )

    @property
    def total_by_sexes(self):
        return self.total_men + self.total_women

    @property
    def total_18_24(self):
        return self.men_18_24 + self.women_18_24

    @property
    def total_25_34(self):
        return self.men_25_34 + self.women_25_34

    @property
    def total_35_44(self):
        return self.men_35_44 + self.women_35_44

    @property
    def total_45_64(self):
        return self.men_45_64 + self.women_45_64

    @property
    def total_65_over(self):
        return self.men_65_over + self.women_65_over

    @property
    def total_by_age_groups(self):
        return (
            self.total_18_24 + self.total_25_34 +
            self.total_35_44 + self.total_44_65 + self.total_65_over
        )

    @classmethod
    def from_dict_csv(cls, voting_information):
        return cls(
            int(voting_information["total_possible_voters"]),
            int(voting_information["total_voters"]),

            int(voting_information["men-18-24"]),
            int(voting_information["men-25-34"]),
            int(voting_information["men-35-44"]),
            int(voting_information["men-45-64"]),
            int(voting_information["men-65-over"]),

            int(voting_information["women-18-24"]),
            int(voting_information["women-25-34"]),
            int(voting_information["women-35-44"]),
            int(voting_information["women-45-64"]),
            int(voting_information["women-65-over"]),
        )

    @classmethod
    def from_dict(cls, voting_information: dict) -> "VotingInformation":
        return cls(
            voting_information["totalPossibleVoters"],
            voting_information["totalVoters"],
            voting_information["men-18-24"],
            voting_information["men-25-34"],
            voting_information["men-35-44"],
            voting_information["men-45-64"],
            voting_information["men-65-over"],
            voting_information["women-18-24"],
            voting_information["women-25-34"],
            voting_information["women-35-44"],
            voting_information["women-45-64"],
            voting_information["women-65-over"],
        )

    def to_dict(self) -> dict:
        return {
            "totalPossibleVoters": self.total_possible_voters,
            "totalVoters": self.total_voters,
            "men-18-24": self.men_18_24,
            "men-25-34": self.men_25_34,
            "men-35-44": self.men_35_44,
            "men-45-64": self.men_45_64,
            "men-65-over": self.men_65_over,
            "women-18-24": self.women_18_24,
            "women-25-34": self.women_25_34,
            "women-35-44": self.women_35_44,
            "women-45-64": self.women_45_64,
            "women-65-over": self.women_65_over,
        }
