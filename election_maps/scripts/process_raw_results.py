from election_maps.clients.db.results_raw import RawResultsDatabaseHandler
from election_maps.clients.db.results import ResultsDatabaseHandler
from election_maps.utils import process_actions

if __name__ == '__main__':
    raw_results_db_handler = RawResultsDatabaseHandler()
    results_db_handler = ResultsDatabaseHandler()

    process_actions(
        results_db_handler=results_db_handler,
        raw_results_db_handler=raw_results_db_handler,
    )
