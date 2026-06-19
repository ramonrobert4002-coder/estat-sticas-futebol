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
    <p>Use: /competitions</p>
    <p>Use: /team?id=ID_DO_TIME</p>
    """

# TESTE DA API
@app.route("/test")
def test():
    url = f"{BASE_URL}/competitions"
    r = requests.get(url, headers=headers)
    return r.json()

# LISTAR COMPETIÇÕES (pra você pegar IDs corretos)
@app.route("/competitions")
def competitions():
    url = f"{BASE_URL}/competitions"
    r = requests.get(url, headers=headers)
    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
@app.route("/brasileirao")
def brasileirao():
    url = f"{BASE_URL}/competitions/2013/matches?limit=10"
    r = requests.get(url, headers=headers)

    data = r.json()
    matches = data.get("matches", [])

    return {
        "jogos_encontrados": len(matches),
        "jogos": matches
    }
