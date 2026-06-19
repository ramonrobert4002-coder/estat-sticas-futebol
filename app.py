from flask import Flask, request
import requests

app = Flask(__name__)

API_KEY = "1e2f241e1846458ab5e8e68f7889bf1f"
BASE_URL = "https://api.football-data.org/v4"

headers = {
    "X-Auth-Token": API_KEY
}

@app.route("/")
def home():
    return """
    <h1>Estatísticas de Futebol</h1>
    <p>Use: /brasileirao</p>
    <p>Use: /team?name=Palmeiras</p>
    """

@app.route("/brasileirao")
def brasileirao():
    url = f"{BASE_URL}/competitions/2013/matches?limit=380"
    r = requests.get(url, headers=headers)

    data = r.json()
    matches = data.get("matches", [])

    gols = 0
    over25 = 0
    btts = 0

    for m in matches:
        home = m["score"]["fullTime"]["home"] or 0
        away = m["score"]["fullTime"]["away"] or 0

        gols += home + away

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

    total = len(matches)

    return {
        "jogos": total,
        "gols_totais": gols,
        "media_gols": gols / total,
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%"
    }

@app.route("/team")
def team():
    name = request.args.get("name")

    if not name:
        return {"erro": "use ?name=Flamengo"}

    url = f"{BASE_URL}/competitions/2013/matches?limit=380"
    r = requests.get(url, headers=headers)

    data = r.json()
    matches = data.get("matches", [])

    filtered = []

    for m in matches:
        home_team = m["homeTeam"]["name"]
        away_team = m["awayTeam"]["name"]

        if name.lower() in home_team.lower() or name.lower() in away_team.lower():
            filtered.append(m)

    filtered = filtered[-10:]

    gols_feitos = 0
    gols_sofridos = 0
    over25 = 0
    btts = 0

    for m in filtered:
        home = m["score"]["fullTime"]["home"] or 0
        away = m["score"]["fullTime"]["away"] or 0

        if name.lower() in m["homeTeam"]["name"].lower():
            gols_feitos += home
            gols_sofridos += away
        else:
            gols_feitos += away
            gols_sofridos += home

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

    total = len(filtered) if filtered else 1

    return {
        "time": name,
        "jogos": total,
        "gols_feitos": gols_feitos,
        "gols_sofridos": gols_sofridos,
        "media_gols_feitos": round(gols_feitos / total, 2),
        "media_gols_sofridos": round(gols_sofridos / total, 2),
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
