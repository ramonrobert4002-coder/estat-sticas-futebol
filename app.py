from flask import Flask
import requests

app = Flask(__name__)

BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

HEADERS = {
    "X-RapidAPI-Key": "SUA_CHAVE_AQUI",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}


@app.route("/")
def home():
    return {
        "mensagem": "API de Estatísticas de Futebol PRO",
        "rotas": {
            "/team/Flamengo": "Estatísticas do Flamengo",
            "/team/Palmeiras": "Estatísticas do Palmeiras",
            "/team/Corinthians": "Estatísticas do Corinthians"
        }
    }


# IDs dos clubes
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


@app.route("/team/<nome>")
def team(nome):

    nome = nome.lower()

    if nome not in TEAMS:
        return {"erro": "Time não encontrado"}

    team_id = TEAMS[nome]

    url = f"{BASE_URL}/fixtures"

    params = {
        "team": team_id,
        "last": 10
    }

    r = requests.get(url, headers=HEADERS, params=params)
    data = r.json()

    jogos = data["response"]

    gols_feitos = 0
    gols_sofridos = 0

    over25 = 0
    btts = 0

    vitorias = 0
    empates = 0
    derrotas = 0

    forma = []

    ultimos = []

    for j in jogos:

        casa_id = j["teams"]["home"]["id"]

        home = j["goals"]["home"] or 0
        away = j["goals"]["away"] or 0

        if casa_id == team_id:
            gf = home
            gs = away
        else:
            gf = away
            gs = home

        gols_feitos += gf
        gols_sofridos += gs

        if gf > gs:
            vitorias += 1
            forma.append("V")
        elif gf == gs:
            empates += 1
            forma.append("E")
        else:
            derrotas += 1
            forma.append("D")

        if home + away > 2:
            over25 += 1

        if home > 0 and away > 0:
            btts += 1

        ultimos.append(
            f'{j["teams"]["home"]["name"]} '
            f'{home} x {away} '
            f'{j["teams"]["away"]["name"]}'
        )

    total = len(jogos)

    aproveitamento = (vitorias * 3 + empates) / (total * 3) * 100

    return {
        "time": nome.title(),
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
        "aproveitamento": f"{aproveitamento:.2f}%",
        "forma": "".join(forma),
        "ultimos_jogos": ultimos
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
