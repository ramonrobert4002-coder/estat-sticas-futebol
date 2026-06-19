from flask import Flask

app = Flask(_name_)

@app.route("/")
def home():
    return """
    <h1>Estatísticas de Futebol</h1>
    <p>Aplicativo criado por Ramon.</p>
    <p>Em breve: médias de gols, over 2.5 e BTTS.</p>
    """

if __name__ == "_main_":
    app.run(host="0.0.0.0", port=10000)
