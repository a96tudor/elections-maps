from typing import Optional

from flask import Flask

from election_maps.clients.db.results_raw import RawResultsDatabaseHandler
from election_maps.clients.db.results import ResultsDatabaseHandler
from election_maps.types import ObserverActionStatusType, VotingSessionType


LOCAL_URL = 'http://127.0.0.1:8000'
SERVER_URL = ''  # TODO: Fill this in once we know where we deploy


def get_api_url(app: Flask) -> str:
    if app.debug:
        return LOCAL_URL
    return SERVER_URL


RESULTS_TO_UPDATE = {
    VotingSessionType.MAYOR: lambda vs: vs.mayor_results,
    VotingSessionType.LOCAL_COUNCIL: lambda vs: vs.local_council_results,
    VotingSessionType.COUNTY_COUNCIL: lambda vs: vs.county_council_results,
    VotingSessionType.COUNTY_COUNCIL_PRESIDENT: (
        lambda vs: vs.county_council_president_results
    ),
}


def process_actions(
    raw_results_db_handler: RawResultsDatabaseHandler,
    results_db_handler: ResultsDatabaseHandler,
    observer_id: Optional[str] = None
):
    if observer_id:
        actions = raw_results_db_handler.get_actions_to_process_by_observer_id(
            observer_id=observer_id
        )
    else:
        actions = raw_results_db_handler.get_actions_to_process()

    if len(actions) == 0:
        return

    raw_results_db_handler.batch_update_status(
        [action.db_id for action in actions], ObserverActionStatusType.PROCESSING,
    )
    try:
        known_voting_sections = {}
        voting_sections = set()

        for key, actions in actions.grouped.items():
            observer_id, session, entity_id = key
            if observer_id not in known_voting_sections:
                voting_section = actions.voting_section_grouped
                known_voting_sections[observer_id] = voting_section
            else:
                voting_section = known_voting_sections[observer_id]

            results_to_update = RESULTS_TO_UPDATE[session](voting_section)
            entity_to_update = results_to_update.get_by_id(entity_id)
            if entity_to_update is None:
                delta = actions.increment_count - actions.decrement_count
                results_to_update.invalid_votes += delta
            else:
                entity_to_update.process_actions(actions)

            voting_sections.add(voting_section)

        for vs in voting_sections:
            results_db_handler.update_section(
                section_number=vs.number,
                results_section=vs.results_as_dict(),
            )

    except Exception as e:
        raw_results_db_handler.batch_update_status(
            [action.db_id for action in actions],
            ObserverActionStatusType.PROCESSING_ERROR,
        )
        raise e

    raw_results_db_handler.batch_update_status(
        [action.db_id for action in actions], ObserverActionStatusType.PROCESSED,
    )
