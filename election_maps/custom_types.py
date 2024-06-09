from enum import Enum


class ObserverActionType(Enum):
    INCREMENT = "INCREMENT"
    DECREMENT = "DECREMENT"


class VotingSessionType(Enum):
    MAYOR = "mayor"
    LOCAL_COUNCIL = "local_council"
    COUNTY_COUNCIL = "county_council"
    COUNTY_COUNCIL_PRESIDENT = "county_council_president"


class ObserverActionStatusType(Enum):
    ACKNOWLEDGED = "ACKNOWLEDGED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    PROCESSING_ERROR = "PROCESSING_ERROR"
