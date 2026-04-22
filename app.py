import os
import re
import csv
import io
import json
from flask import Flask, render_template, request, Response
from playwright.sync_api import sync_playwright
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Configuración del modelo BERT Multilingüe para análisis de sentimientos
# Se mantiene este modelo por su alta precisión en español e inglés
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

def analizar_sentimiento_pro(comentarios):
    if not comentarios:
        return "Neutro"
    
    puntuaciones = []
    for texto in comentarios:
        try:
            # El modelo BERT devuelve etiquetas de '1 star' a '5 stars'
            res = sentiment_pipeline(texto[:512])[0]
            score = int(res['label'].split()[0])
            
            # Mapeo de estrellas a valores numéricos para promedio
            if score >= 4: puntuaciones.append(1)   # Positivo
            elif score <= 2: puntuaciones.append(-1) # Negativo
            else: puntuaciones.append(0)             # Neutro
        except:
            continue

    if not puntuaciones: return "Neutro"
    promedio = sum(puntuaciones) / len(puntuaciones)
    
    # Umbrales para determinar el sentimiento general del post
    if promedio > 0.2: return "Positivo"
    elif promedio < -0.2: return "Negativo"
    return "Neutro"

def obtener_posts(username, cantidad):
    posts_data = []
    with sync_playwright() as p:
        # headless=True para ejecución en segundo plano (ideal para producción/QA)
        browser = p.chromium.launch(headless=True)
        # Importante: Requiere que login.py haya generado state.json satisfactoriamente
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        try:
            page.goto(f"https://www.instagram.com/{username}/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector('a[href*="/p/"]', timeout=15000)
            
            # Scroll suave para asegurar que los elementos se rendericen
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(2000)
            
            posts = page.query_selector_all('a[href*="/p/"]')

            for post in posts[:cantidad]:
                try:
                    post.click()
                    page.wait_for_timeout(3000)

                    # Extracción de Likes con Regex (soporta inglés y español)
                    likes = "0"
                    likes_element = page.locator('section').filter(has_text=re.compile(r'likes|me gusta', re.I)).first
                    if likes_element.is_visible():
                        text_likes = likes_element.inner_text()
                        match = re.search(r'([\d.,]+)', text_likes)
                        likes = match.group(1) if match else "0"

                    # Captura de comentarios significativos para la IA
                    comment_spans = page.query_selector_all('ul li span')
                    comentarios_texto = [s.inner_text() for s in comment_spans if len(s.inner_text()) > 5][:8]

                    sentimiento = analizar_sentimiento_pro(comentarios_texto)

                    posts_data.append({
                        "likes": likes,
                        "comentarios": len(comentarios_texto),
                        "sentimiento": sentimiento
                    })

                    page.keyboard.press("Escape")
                    page.wait_for_timeout(1000)
                except:
                    page.keyboard.press("Escape")
        except Exception as e:
            print(f"Error detectado en el Scraper: {e}")
        finally:
            browser.close()
    return posts_data

@app.route("/", methods=["GET", "POST"])
def index():
    posts = []
    if request.method == "POST":
        user = request.form.get("username").replace("@", "").strip()
        cant = int(request.form.get("cantidad", 5))
        posts = obtener_posts(user, cant)
    return render_template("index.html", posts=posts)

@app.route("/descargar_csv", methods=["POST"])
def descargar_csv():
    datos_raw = request.form.get("datos_json")
    if not datos_raw: 
        return "No hay datos para exportar", 400
        
    posts = json.loads(datos_raw)
    
    # Creación del archivo CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Post #', 'Likes', 'Comentarios', 'Sentimiento'])
    
    for i, p in enumerate(posts, 1):
        writer.writerow([i, p['likes'], p['comentarios'], p['sentimiento']])
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=reporte_instagram.csv"}
    )

if __name__ == "__main__":
    # debug=True es útil para desarrollo, cámbialo a False en PROD
    app.run(debug=True)