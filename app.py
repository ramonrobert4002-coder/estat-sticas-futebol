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
    return {
        "mensagem": "API de Estatísticas de Futebol (PRO)",
        "rotas": {
            "/competitions": "Lista ligas",
            "/team?id=ID": "Estatísticas do time"
        }
    }


@app.route("/competitions")
def competitions():
    url = f"{BASE_URL}/competitions"
    r = requests.get(url, headers=headers)
    return r.json()


@app.route("/team")
def team():

    team_id = request.args.get("id")

    if not team_id:
        return {"erro": "use ?id=2017"}

    url = f"{BASE_URL}/teams/{team_id}/matches?limit=10"
    r = requests.get(url, headers=headers)

    data = r.json()
    matches = data.get("matches", [])

    if not matches:
        return {"erro": "nenhum jogo encontrado para esse time"}

    gols_feitos = 0
    gols_sofridos = 0
    over25 = 0
    btts = 0

    jogos = []

    for m in matches:

        home = m["score"]["fullTime"]["home"] or 0
        away = m["score"]["fullTime"]["away"] or 0

        gols_feitos += home + away

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

        jogos.append({
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"],
            "placar": f"{home} x {away}",
            "status": m["status"]
        })

    total = len(matches)

    return {
        "team_id": team_id,
        "jogos": total,
        "gols_totais": gols_feitos,
        "media_gols": round(gols_feitos / total, 2),
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%",
        "ultimos_jogos": jogos
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
