from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = "1e2f241e1846458ab5e8e68f7889bf1f"
BASE_URL = "https://api.football-data.org/v4"

headers = {
    "X-Auth-Token": API_KEY
}


# --------------------------------
# PÁGINA INICIAL
# --------------------------------
@app.route("/")
def home():
    return {
        "mensagem": "API de Estatísticas de Futebol (PRO)",
        "rotas": {
            "/competitions": "Lista ligas",
            "/brasileirao": "Estatísticas gerais do Brasileirão",
            "/team/Flamengo": "Estatísticas do Flamengo",
            "/team/Palmeiras": "Estatísticas do Palmeiras"
        }
    }


# --------------------------------
# TESTE DA API
# --------------------------------
@app.route("/test")
def test():
    try:
        r = requests.get(
            f"{BASE_URL}/competitions",
            headers=headers,
            timeout=10
        )
        return jsonify(r.json())
    except Exception as e:
        return {"erro": str(e)}


# --------------------------------
# COMPETIÇÕES
# --------------------------------
@app.route("/competitions")
def competitions():
    try:
        r = requests.get(
            f"{BASE_URL}/competitions",
            headers=headers,
            timeout=10
        )
        return jsonify(r.json())
    except Exception as e:
        return {"erro": str(e)}


# --------------------------------
# ESTATÍSTICAS DO BRASILEIRÃO
# --------------------------------
@app.route("/brasileirao")
def brasileirao():

    try:
        url = f"{BASE_URL}/competitions/2013/matches?limit=380"

        r = requests.get(
            url,
            headers=headers,
            timeout=10
        )

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

        if total == 0:
            return {"erro": "Nenhum jogo encontrado"}

        return {
            "jogos": total,
            "gols_totais": gols,
            "media_gols": round(gols / total, 2),
            "over_2_5": f"{(over25 / total) * 100:.2f}%",
            "btts": f"{(btts / total) * 100:.2f}%"
        }

    except Exception as e:
        return {"erro": str(e)}


# --------------------------------
# ESTATÍSTICAS DO TIME
# Exemplo:
# /team/Flamengo
# --------------------------------
@app.route("/team/<name>")
def team(name):

    try:

        url = f"{BASE_URL}/competitions/2013/matches?limit=380"

        r = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        data = r.json()

        matches = data.get("matches", [])

        filtered = []

        for m in matches:

            home_team = m["homeTeam"]["name"]
            away_team = m["awayTeam"]["name"]

            if (
                name.lower() in home_team.lower()
                or
                name.lower() in away_team.lower()
            ):
                filtered.append(m)

        filtered = filtered[-10:]

        if len(filtered) == 0:
            return {
                "erro": f"Time '{name}' não encontrado"
            }

        gols_feitos = 0
        gols_sofridos = 0
        over25 = 0
        btts = 0

        ultimos_jogos = []

        for m in filtered:

            home_goals = m["score"]["fullTime"]["home"] or 0
            away_goals = m["score"]["fullTime"]["away"] or 0

            home_name = m["homeTeam"]["name"]
            away_name = m["awayTeam"]["name"]

            if name.lower() in home_name.lower():
                gols_feitos += home_goals
                gols_sofridos += away_goals
            else:
                gols_feitos += away_goals
                gols_sofridos += home_goals

            if home_goals + away_goals > 2:
                over25 += 1

            if home_goals > 0 and away_goals > 0:
                btts += 1

            ultimos_jogos.append({
                "jogo": f"{home_name} {home_goals} x {away_goals} {away_name}",
                "status": m["status"]
            })

        total = len(filtered)

        return {
            "time": name,
            "jogos": total,
            "gols_feitos": gols_feitos,
            "gols_sofridos": gols_sofridos,
            "media_gols_feitos": round(gols_feitos / total, 2),
            "media_gols_sofridos": round(gols_sofridos / total, 2),
            "over_2_5": f"{(over25 / total) * 100:.2f}%",
            "btts": f"{(btts / total) * 100:.2f}%",
            "ultimos_jogos": ultimos_jogos
        }

    except Exception as e:
        return {"erro": str(e)}


# --------------------------------
# RODAR LOCALMENTE
# --------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
