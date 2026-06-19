from flask import Flask, request
import requests

app = Flask(__name__)

BASE_URL = "https://api.sofascore.com/api/v1"

headers = {
    "User-Agent": "Mozilla/5.0"
}

@app.route("/")
def home():
    return """
    <h1>Estatísticas Sofascore</h1>
    <p>Use: /team?id=2017</p>
    """

@app.route("/team")
def team():
    team_id = request.args.get("id")

    if not team_id:
        return {"erro": "use ?id=2017"}

    url = f"{BASE_URL}/team/{team_id}/events/last/10"
    r = requests.get(url, headers=headers)

    data = r.json()
    events = data.get("events", [])

    gols_feitos = 0
    gols_sofridos = 0
    over25 = 0
    btts = 0

    for e in events:
        home = e["homeScore"].get("current", 0)
        away = e["awayScore"].get("current", 0)

        gols_feitos += home
        gols_sofridos += away

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

    total = len(events) if events else 1

    return {
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
