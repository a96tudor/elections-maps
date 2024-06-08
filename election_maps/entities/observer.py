from typing import Optional

class Observer:

    def __init__(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        voting_section_number: str,
        db_id: Optional[str] = None
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.voting_section_number = voting_section_number
        self.db_id = db_id

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
        db_id = None
        if observer.get("_id"):
            db_id = str(observer.get("_id"))

        return cls(
            first_name=observer["firstName"],
            last_name=observer["lastName"],
            phone_number=observer["phoneNumber"],
            voting_section_number=observer["votingSectionNumber"],
            db_id=db_id,
        )

    def to_dict(self) -> dict:
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phoneNumber": self.phone_number,
            "votingSectionNumber": self.voting_section_number,
        }
