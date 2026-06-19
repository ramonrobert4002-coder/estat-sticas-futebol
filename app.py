from flask import Flask
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

TEAMS = {
    "flamengo": 127,
    "palmeiras": 131,
    "corinthians": 126,
    "santos": 135,
    "vasco": 139,
    "gremio": 121,
    "internacional": 119,
    "bahia": 118,
    "cruzeiro": 124,
    "atletico-mg": 1062
}


@app.route("/")
def home():
    return {
        "mensagem": "API de Estatísticas de Futebol PRO",
        "rotas": {
            "/team/flamengo": "Estatísticas do Flamengo",
            "/team/palmeiras": "Estatísticas do Palmeiras"
        }
    }


@app.route("/team/<nome>")
def team(nome):

    nome = nome.lower()

    if nome not in TEAMS:
        return {"erro": "Time não encontrado"}

    if not API_KEY:
        return {"erro": "RAPIDAPI_KEY não configurada no Render"}

    team_id = TEAMS[nome]

    params = {
        "team": team_id,
        "last": 10
    }

    response = requests.get(
        f"{BASE_URL}/fixtures",
        headers=HEADERS,
        params=params,
        timeout=20
    )

    data = response.json()

    if "response" not in data:
        return data

    jogos = data["response"]

    gols_feitos = 0
    gols_sofridos = 0
    vitorias = 0
    empates = 0
    derrotas = 0
    over25 = 0
    btts = 0

    ultimos = []

    for j in jogos:

        home_id = j["teams"]["home"]["id"]

        home_goals = j["goals"]["home"] or 0
        away_goals = j["goals"]["away"] or 0

        if home_id == team_id:
            gf = home_goals
            gs = away_goals
        else:
            gf = away_goals
            gs = home_goals

        gols_feitos += gf
        gols_sofridos += gs

        if gf > gs:
            vitorias += 1
        elif gf == gs:
            empates += 1
        else:
            derrotas += 1

        if (home_goals + away_goals) > 2:
            over25 += 1

        if home_goals > 0 and away_goals > 0:
            btts += 1

        ultimos.append(
            f'{j["teams"]["home"]["name"]} '
            f'{home_goals} x {away_goals} '
            f'{j["teams"]["away"]["name"]}'
        )

    total = len(jogos)

    return {
        "time": nome.title(),
        "jogos": total,
        "vitorias": vitorias,
        "empates": empates,
        "derrotas": derrotas,
        "gols_feitos": gols_feitos,
        "gols_sofridos": gols_sofridos,
        "media_gols_feitos": round(gols_feitos / total, 2) if total else 0,
        "media_gols_sofridos": round(gols_sofridos / total, 2) if total else 0,
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%",
        "ultimos_jogos": ultimos
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
