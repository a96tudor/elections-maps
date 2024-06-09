from flask import render_template, redirect

from election_maps.clients.db.users import UsersDatabaseHandler
from election_maps.clients.db.results import ResultsDatabaseHandler
from election_maps.clients.db.results_raw import RawResultsDatabaseHandler
from election_maps.utils import process_actions


def build_counting_user_page(
    users_db_handler: UsersDatabaseHandler,
    results_db_handler: ResultsDatabaseHandler,
    raw_results_db_handler: RawResultsDatabaseHandler,
    user_id: str,
    api_url: str,
    **kwargs,
):
    try:
        observer = users_db_handler.get_user_by_id(user_id)
    except Exception:
        return redirect("/numarare")

    if observer:
        process_actions(raw_results_db_handler, results_db_handler, user_id)
        try:
            voting_section_status = results_db_handler.get_voting_section_by_number(
                observer.voting_section_number
            )
        except Exception:
            return redirect("/numarare")

        invalid_votes = {
            "mayor": voting_section_status.mayor_results.invalid_votes,
            "local_council": voting_section_status.local_council_results.invalid_votes,
            "county_council": (
                voting_section_status.county_council_results.invalid_votes
            ),
            "county_council_president": (
                voting_section_status.county_council_president_results.invalid_votes
            ),
            "european_parliament": (
                voting_section_status.european_parliament_results.invalid_votes
            )
        }

        return render_template(
            "reports.html",
            observer=observer,
            mayor_candidates=voting_section_status.mayor_results,
            local_council_candidates=voting_section_status.local_council_results,
            county_council_candidates=voting_section_status.county_council_results,
            county_council_president_candidates=(
                voting_section_status.county_council_president_results
            ),
            european_parliament_candidates=(
                voting_section_status.european_parliament_results
            ),
            invalid_votes=invalid_votes,
            api_url=api_url,
            **kwargs,
        )
    else:
        return redirect("/numarare")
