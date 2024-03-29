import flask
from threading import Thread

from rating import startRating as initRating, rate as rateGirls
from ranking import generate_rankings

app = flask.Flask(__name__)


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


@app.route("/getRankings/getGirlRankings/", methods=["GET"])
def getGirlRankings():
    rankings = generate_rankings()
    return flask.jsonify(rankings)


@app.route("/getRankings", methods=["GET"])
def getRankings():
    return flask.render_template("ranks.html")


def run():
    app.run(port="80", host="0.0.0.0")


def keep_alive():
    server = Thread(target=run)
    server.start()


if __name__ == "__main__":
    keep_alive()
