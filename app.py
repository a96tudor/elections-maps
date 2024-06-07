from flask import Flask, render_template

from election_maps.entities.observer import Observer

app = Flask(__name__)


@app.route('/numarare')
def count():
    dummy_observer = Observer("John", "Doe", "1234455677", "12")
    return render_template("reports.html", observer=dummy_observer)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)
