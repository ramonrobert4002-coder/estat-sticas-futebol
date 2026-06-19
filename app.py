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
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        if name.lower() in home.lower() or name.lower() in away.lower():
            filtered.append(m)

    filtered = filtered[-10:]  # últimos 10 jogos

    gols_feitos = 0
    gols_sofridos = 0
    over25 = 0
    btts = 0

    for m in filtered:
        home = m["score"]["fullTime"]["home"] or 0
        away = m["score"]["fullTime"]["away"] or 0

        # identifica se o time é casa ou fora
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
        "media_gols": gols_feitos / total,
        "over_2_5": f"{(over25 / total) * 100:.2f}%",
        "btts": f"{(btts / total) * 100:.2f}%"
    }
    
