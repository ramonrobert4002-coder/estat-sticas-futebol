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
    <p>Use: /test</p>
    <p>Use: /competitions</p>
    <p>Use: /brasileirao</p>
    """

@app.route("/test")
def test():
    url = f"{BASE_URL}/competitions"
    r = requests.get(url, headers=headers)
    return r.json()

@app.route("/competitions")
def competitions():
    url = f"{BASE_URL}/competitions"
    r = requests.get(url, headers=headers)
    return r.json()

@app.route("/brasileirao")
def brasileirao():
    url = f"{BASE_URL}/competitions/2013/matches?limit=10"
    r = requests.get(url, headers=headers)

    data = r.json()
    matches = data.get("matches", [])

    gols = 0
    sofridos = 0
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

    total = len(matches) if matches else 1

    return {
        "jogos": total,
        "gols_totais": gols,
        "media_gols": gols / total,
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%"
    
