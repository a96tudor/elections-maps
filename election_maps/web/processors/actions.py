from flask import Response

from election_maps.custom_types import VotingSessionType, ObserverActionType
from election_maps.clients.db.results_raw import RawResultsDatabaseHandler
from election_maps.clients.db.users import UsersDatabaseHandler
from election_maps.entities.action import ObserverAction


def process_post_action_request(
    observer_id: str,
    request_body: dict,
    raw_results_db_handler: RawResultsDatabaseHandler,
    users_db_handler: UsersDatabaseHandler,
) -> Response:
    try:
        user = users_db_handler.get_user_by_id(observer_id)
        if user is None:
            return Response(status=403, response="Unauthorized")

        session_type = VotingSessionType(request_body["sessionType"])
        action_type = ObserverActionType(request_body["actionType"])

        action = ObserverAction(
            observer_id=observer_id,
            action_type=action_type,
            voting_session=session_type,
            entity_id=request_body["entityId"]
        )

        raw_results_db_handler.add_one_action(action)

        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=500)
