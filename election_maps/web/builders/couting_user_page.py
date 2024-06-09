from flask import render_template, redirect

from election_maps.clients.db.users import UsersDatabaseHandler
from election_maps.clients.db.results import ResultsDatabaseHandler


def build_counting_user_page(
    users_db_handler: UsersDatabaseHandler,
    user_id: str,
    results_db_handler: ResultsDatabaseHandler,
):
    try:
        observer = users_db_handler.get_user_by_id(user_id)
    except Exception:
        return redirect("/numarare")

    if observer:
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
            invalid_votes=invalid_votes,
        )
    else:
        return redirect("/numarare")
