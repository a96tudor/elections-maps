from flask import Flask, render_template, request, redirect

from election_maps.clients.db.users import UsersDatabaseHandler

app = Flask(__name__, static_folder='static', template_folder='templates')
users_db_handler = None


@app.route('/numarare/<user_id>', methods=["GET"])
def count_main(user_id):
    observer = users_db_handler.get_user_by_id(user_id)
    print(user_id)
    print(observer)

    if observer:
        return render_template("reports.html", observer=observer)
    else:
        return redirect("/numarare")


@app.route('/numarare', methods=["POST"])
def count_post():
    global users_db_handler
    phone_number = request.values.get("phone")

    observer = users_db_handler.get_user_by_phone_number(phone_number)
    print(observer)

    if observer is None:
        return redirect("/numarare")
    else:
        return redirect(f"/numarare/{observer.db_id}")


@app.route('/numarare', methods=["GET"])
def count_home():
    return render_template("phone_number_form.html")


if __name__ == '__main__':
    users_db_handler = UsersDatabaseHandler()
    app.run(host="0.0.0.0", debug=True, port=3000)
