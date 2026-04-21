from flask import Flask, render_template, request
import requests
from textblob import TextBlob

app = Flask(__name__)

def analizar_sentimiento(texto):
    if not texto:
        return "Neutro"
    
    analisis = TextBlob(texto)
    polaridad = analisis.sentiment.polarity

    if polaridad > 0:
        return "Positivo"
    elif polaridad < 0:
        return "Negativo"
    else:
        return "Neutro"


def obtener_posts(username, cantidad):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "x-ig-app-id": "936619743392459"
    }

    response = requests.get(url, headers=headers)

    posts_data = []

    if response.status_code == 200:
        data = response.json()
        posts = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

        for post in posts[:cantidad]:
            node = post["node"]

            # Intentar obtener primer comentario
            comentarios_lista = node.get("edge_media_to_comment", {}).get("edges", [])
            texto_comentario = ""

            if comentarios_lista:
                texto_comentario = comentarios_lista[0].get("node", {}).get("text", "")

            sentimiento = analizar_sentimiento(texto_comentario)

            posts_data.append({
                "id": node["id"],
                "likes": node["edge_liked_by"]["count"],
                "comentarios": node["edge_media_to_comment"]["count"],
                "sentimiento": sentimiento
            })

    return posts_data


@app.route("/", methods=["GET", "POST"])
def index():
    posts = []
    username = ""
    cantidad = 10

    if request.method == "POST":
        username = request.form["username"]
        cantidad = int(request.form["cantidad"])
        posts = obtener_posts(username, cantidad)

    return render_template("index.html", posts=posts, username=username, cantidad=cantidad)


if __name__ == "__main__":
    app.run(debug=True)