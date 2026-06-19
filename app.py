from flask import Flask, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://api.football-data.org/v4"
API_KEY = "1e2f241e1846458ab5e8e68f7889bf1f"

headers = {
    "X-Auth-Token": API_KEY
}

# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return {
        "mensagem": "API de Estatísticas de Futebol (PRO)",
        "rotas": {
            "/competitions": "Lista de ligas",
            "/team/<nome>": "Estatísticas do time (ex: /team/Flamengo)"
        }
    }


# -----------------------------
# COMPETITIONS
# -----------------------------
@app.route("/competitions")
def competitions():
    try:
        r = requests.get(f"{BASE_URL}/competitions", headers=headers, timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return {"erro": str(e)}


# -----------------------------
# TEAM STATS
# -----------------------------
@app.route("/team/<name>")
def team(name):

    try:
        url = f"{BASE_URL}/competitions/2013/matches?limit=380"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        matches = data.get("matches", [])

        filtered = [
            m for m in matches
            if name.lower() in m["homeTeam"]["name"].lower()
            or name.lower() in m["awayTeam"]["name"].lower()
        ]

        last_matches = filtered[-5:]

        gols_feitos = 0
        gols_sofridos = 0
        over25 = 0
        btts = 0

        jogos_formatados = []

        for m in last_matches:
            home = m["score"]["fullTime"]["home"] or 0
            away = m["score"]["fullTime"]["away"] or 0

            home_name = m["homeTeam"]["name"]
            away_name = m["awayTeam"]["name"]

            # identifica lado do time
            if name.lower() in home_name.lower():
                gols_feitos += home
                gols_sofridos += away
            else:
                gols_feitos += away
                gols_sofridos += home

            if home + away > 2:
                over25 += 1

            if home > 0 and away > 0:
                btts += 1

            jogos_formatados.append({
                "jogo": f"{home_name} {home} x {away} {away_name}",
                "data": m["utcDate"],
                "status": m["status"]
            })

        total = len(last_matches) if last_matches else 1

        return {
            "time": name,
            "jogos_analisados": total,
            "gols_feitos": gols_feitos,
            "gols_sofridos": gols_sofridos,
            "media_gols_feitos": round(gols_feitos / total, 2),
            "media_gols_sofridos": round(gols_sofridos / total, 2),
            "over_2_5": f"{(over25 / total) * 100:.2f}%",
            "btts": f"{(btts / total) * 100:.2f}%",
            "ultimos_jogos": jogos_formatados
        }

    except Exception as e:
        return {"erro": str(e)}


# -----------------------------
# RUN LOCAL (Render ignora isso)
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    git add .
git commit -m "API PRO melhorada"
git push
