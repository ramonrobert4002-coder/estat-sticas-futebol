from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = "1e2f241e1846458ab5e8e68f7889bf1f"
BASE_URL = "https://api.football-data.org/v4"

headers = {
    "X-Auth-Token": API_KEY
}

def get_last_matches(team_id):
    url = f"{BASE_URL}/teams/{team_id}/matches?limit=10"
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/")
def home():
    return """
    <h1>Estatísticas de Futebol</h1>
    <p>Use /team?id=ID_DO_TIME</p>
    """

@app.route("/team")
def team_stats():
    team_id = request.args.get("id")

    if not team_id:
        return {"error": "envie ?id=TIME_ID"}

    data = get_last_matches(team_id)

    matches = data.get("matches", [])

    goals_for = 0
    goals_against = 0
    total_games = len(matches)

    over25 = 0
    btts = 0

    for m in matches:
        home = m["score"]["fullTime"]["home"] or 0
        away = m["score"]["fullTime"]["away"] or 0

        goals_for += home
        goals_against += away

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

    return {
        "jogos": total_games,
        "gols_feitos": goals_for,
        "gols_sofridos": goals_against,
        "media_gols_feitos": goals_for / total_games if total_games else 0,
        "media_gols_sofridos": goals_against / total_games if total_games else 0,
        "over_2_5": f"{(over25 / total_games) * 100 if total_games else 0:.2f}%",
        "btts": f"{(btts / total_games) * 100 if total_games else 0:.2f}%"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
