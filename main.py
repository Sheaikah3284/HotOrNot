import flask

from rating import startRating as initRating, rate as rateGirls
from ranking import generate_rankings

app = flask.Flask(__name__)
app.config["PORT"] = 80


@app.route('/', methods=['GET'])
def home():
    return flask.render_template("index.html")


@app.route("/startRating", methods=["POST"])
def startRating():
    rating_data = initRating()
    return flask.jsonify(rating_data)


@app.route("/rate", methods=["POST"])
def rate():
    winner = flask.request.json["winner"]
    loser = flask.request.json["loser"]

    winner = int(winner)
    loser = int(loser)

    rateGirls(winner, loser)

    # return 200 OK and body with message
    return flask.jsonify(initRating())


@app.route("/getRankings", methods=["GET"])
def getRankings():
    rankings = generate_rankings()
    return flask.jsonify(rankings)


app.run(port=app.config["PORT"])
