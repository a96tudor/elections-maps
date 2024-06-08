from election_maps.clients.db.base import BaseDatabaseHandler


class ResultsDatabaseHandler(BaseDatabaseHandler):
    def __init__(self):
        super().__init__("results_collection")
