from flask import Flask
import requests

app = Flask(__name__)

BASE_URL = "https://api.football-data.org/v4"
API_KEY = "1e2f241e1846458ab5e8e68f7889bf1f"

headers = {
    "X-Auth-Token": API_KEY
}


@app.route("/")
def home():
    return {
        "mensagem": "API de Estatísticas de Futebol (PRO)",
        "rotas": {
            "/competitions": "Lista ligas",
            "/brasileirao": "Estatísticas gerais do Brasileirão",
            "/team/Palmeiras": "Estatísticas do Palmeiras",
            "/team/Flamengo": "Estatísticas do Flamengo"
        }
    }


@app.route("/competitions")
def competitions():
    url = f"{BASE_URL}/competitions"
    r = requests.get(url, headers=headers)
    return r.json()


@app.route("/brasileirao")
def brasileirao():
    url = f"{BASE_URL}/competitions/2013/matches"
    r = requests.get(url, headers=headers)

    data = r.json()
    matches = data.get("matches", [])

    jogos = [m for m in matches if m["status"] == "FINISHED"]

    gols = 0
    over25 = 0
    btts = 0

    for m in jogos:
        home = m["score"]["fullTime"]["home"] or 0
        away = m["score"]["fullTime"]["away"] or 0

        gols += home + away

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

    total = len(jogos) if jogos else 1

    return {
        "jogos": total,
        "gols_totais": gols,
        "media_gols": round(gols / total, 2),
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%"
    }


@app.route("/team/<name>")
def team(name):

    url = f"{BASE_URL}/competitions/2013/matches"
    r = requests.get(url, headers=headers)

    data = r.json()
    matches = data.get("matches", [])

    filtered = []

    for m in matches:
        home_team = m["homeTeam"]["name"]
        away_team = m["awayTeam"]["name"]

        if (
            name.lower() in home_team.lower()
            or name.lower() in away_team.lower()
        ) and m["status"] == "FINISHED":
            filtered.append(m)

    filtered = filtered[-10:]

    gols_feitos = 0
    gols_sofridos = 0
    over25 = 0
    btts = 0
    vitorias = 0
    empates = 0
    derrotas = 0

    ultimos_jogos = []

    for m in filtered:

        home_team = m["homeTeam"]["name"]
        away_team = m["awayTeam"]["name"]

        home = m["score"]["fullTime"]["home"] or 0
        away = m["score"]["fullTime"]["away"] or 0

        ultimos_jogos.append(
            f"{home_team} {home} x {away} {away_team}"
        )

        if name.lower() in home_team.lower():

            gols_feitos += home
            gols_sofridos += away

            if home > away:
                vitorias += 1
            elif home == away:
                empates += 1
            else:
                derrotas += 1

        else:

            gols_feitos += away
            gols_sofridos += home

            if away > home:
                vitorias += 1
            elif away == home:
                empates += 1
            else:
                derrotas += 1

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

    total = len(filtered)

    if total == 0:
        return {
            "erro": "Nenhum jogo finalizado encontrado para esse time."
        }

    return {
        "time": name,
        "jogos": total,
        "vitorias": vitorias,
        "empates": empates,
        "derrotas": derrotas,
        "gols_feitos": gols_feitos,
        "gols_sofridos": gols_sofridos,
        "media_gols_feitos": round(gols_feitos / total, 2),
        "media_gols_sofridos": round(gols_sofridos / total, 2),
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%",
        "ultimos_jogos": ultimos_jogos
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
