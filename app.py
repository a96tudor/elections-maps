from flask import Flask, render_template, request, redirect

from election_maps.clients.db.users import UsersDatabaseHandler
from election_maps.clients.db.results import ResultsDatabaseHandler
from election_maps.clients.db.results_raw import RawResultsDatabaseHandler
from election_maps.web.builders.couting_user_page import build_counting_user_page
from election_maps.web.processors.actions import process_post_action_request
from election_maps.utils import get_api_url

app = Flask(__name__, static_folder='static', template_folder='templates')
users_db_handler = None
results_db_handler = None
raw_results_db_handler = None


@app.route("/numarare/action/<user_id>", methods=["POST"])
def add_action(user_id):
    return process_post_action_request(
        observer_id=user_id, request_body=request.json,
        raw_results_db_handler=raw_results_db_handler,
        users_db_handler=users_db_handler,
    )


@app.route('/numarare/<user_id>', methods=["GET"])
def count_main(user_id):
    return build_counting_user_page(
        users_db_handler=users_db_handler,
        user_id=user_id,
        results_db_handler=results_db_handler,
        api_url=get_api_url(app),
        raw_results_db_handler=raw_results_db_handler,
    )


@app.route('/numarare', methods=["POST"])
def count_post():
    phone_number = request.values.get("phone")

    observer = users_db_handler.get_user_by_phone_number(phone_number)

    if observer is None:
        return redirect("/numarare")
    else:
        return redirect(f"/numarare/{observer.db_id}")


@app.route('/numarare', methods=["GET"])
def count_home():
    return render_template("phone_number_form.html")


if __name__ == '__main__':
    users_db_handler = UsersDatabaseHandler()
    results_db_handler = ResultsDatabaseHandler()
    raw_results_db_handler = RawResultsDatabaseHandler()
    app.run(host="0.0.0.0", debug=True, port=8000)
