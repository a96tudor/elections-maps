class Observer:

    def __init__(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        voting_section_number: str
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.voting_section_number = voting_section_number

    @classmethod
    def from_dict_csv(cls, observer: dict) -> "Observer":
        return cls(
            first_name=observer["Prenume"],
            last_name=observer["Nume"],
            phone_number=observer["Numar"],
            voting_section_number=observer["Sectie"]
        )

    @classmethod
    def from_dict(cls, observer: dict) -> "Observer":
        return cls(
            first_name=observer["firstName"],
            last_name=observer["lastName"],
            phone_number=observer["phoneNumber"],
            voting_section_number=observer["votingSectionNumber"]
        )

    def to_dict(self) -> dict:
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phoneNumber": self.phone_number,
            "votingSectionNumber": self.voting_section_number,
        }
