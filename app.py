import os
import re
import csv
import io
import json
import datetime
from flask import Flask, render_template, request, Response
from playwright.sync_api import sync_playwright
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Configuración del modelo BERT Multilingüe
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
            res = sentiment_pipeline(texto[:512])[0]
            score = int(res['label'].split()[0])
            if score >= 4: puntuaciones.append(1)   # Positivo
            elif score <= 2: puntuaciones.append(-1) # Negativo
            else: puntuaciones.append(0)             # Neutro
        except:
            continue

    if not puntuaciones: return "Neutro"
    promedio = sum(puntuaciones) / len(puntuaciones)
    
    if promedio > 0.2: return "Positivo"
    elif promedio < -0.2: return "Negativo"
    return "Neutro"

def obtener_posts(username, cantidad):
    posts_data = []
    fecha_extraccion = datetime.datetime.now().isoformat() + "Z"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Asegúrate de que state.json exista en la raíz del proyecto
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        try:
            # Navegar al perfil
            page.goto(f"https://www.instagram.com/{username}/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector('a[href*="/p/"]', timeout=15000)
            
            # Scroll para cargar elementos
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(2000)
            
            enlaces = page.query_selector_all('a[href*="/p/"]')
            urls = [f"https://www.instagram.com{e.get_attribute('href')}" for e in enlaces[:cantidad]]

            for url in urls:
                try:
                    page.goto(url, wait_until="networkidle")
                    page.wait_for_timeout(2000)

                    # 1. Obtener Descripción para extraer Tags y Menciones
                    desc_element = page.query_selector('h1, span._ap3a')
                    descripcion = desc_element.inner_text() if desc_element else ""
                    
                    hashtags = re.findall(r'#(\w+)', descripcion)
                    menciones = [f"@{m}" for m in re.findall(r'@(\w+)', descripcion)]

                    # 2. Tipo de Contenido
                    tipo = "video" if page.query_selector('video') else "imagen"

                    # 3. Fecha del Post
                    time_element = page.query_selector('time')
                    fecha_iso = time_element.get_attribute('datetime') if time_element else ""

                    # 4. Likes
                    likes = "0"
                    likes_element = page.locator('section').filter(has_text=re.compile(r'likes|me gusta', re.I)).first
                    if likes_element.is_visible():
                        text_likes = likes_element.inner_text()
                        match = re.search(r'([\d.,]+)', text_likes)
                        likes = match.group(1) if match else "0"

                    # 5. Análisis de Sentimiento con BERT
                    comment_spans = page.query_selector_all('ul li span')
                    comentarios_texto = [s.inner_text() for s in comment_spans if len(s.inner_text()) > 5][:8]
                    sentimiento = analizar_sentimiento_pro(comentarios_texto)

                    posts_data.append({
                        "url": url,
                        "tipo": tipo,
                        "likes": likes,
                        "fecha": fecha_iso,
                        "hashtags": hashtags,
                        "menciones": menciones,
                        "sentimiento": sentimiento,
                        "descripcion": descripcion[:100] + "..." # Opcional: resumen
                    })

                except Exception as e:
                    print(f"Error procesando post {url}: {e}")
                    continue

            return {
                "fechaExtraccion": fecha_extraccion,
                "perfil": username,
                "total": len(urls),
                "exitosos": len(posts_data),
                "publicaciones": posts_data
            }

        except Exception as e:
            print(f"Error en Scraper: {e}")
            return None
        finally:
            browser.close()

@app.route("/", methods=["GET", "POST"])
def index():
    posts = None
    if request.method == "POST":
        user = request.form.get("username").replace("@", "").strip()
        cant = int(request.form.get("cantidad", 5))
        posts = obtener_posts(user, cant)
    return render_template("index.html", posts=posts)

@app.route("/descargar_csv", methods=["POST"])
def descargar_csv():
    datos_raw = request.form.get("datos_json")
    if not datos_raw: 
        return "No hay datos", 400
        
    publicaciones = json.loads(datos_raw)
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeceras completas
    writer.writerow(['Fecha', 'Tipo', 'Likes', 'URL', 'Sentimiento', 'Hashtags', 'Menciones'])
    
    for p in publicaciones:
        writer.writerow([
            p.get('fecha', '').split('T')[0],
            p.get('tipo', 'imagen'),
            p.get('likes', '0'),
            p.get('url', ''),
            p.get('sentimiento', 'Neutro'),
            ", ".join(p.get('hashtags', [])),
            ", ".join(p.get('menciones', []))
        ])
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=analisis_instagram.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)