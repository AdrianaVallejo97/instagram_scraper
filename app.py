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

# Pipeline de IA optimizado
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

def analizar_sentimiento_pro(comentarios):
    if not comentarios: return "Neutro"
    puntuaciones = []
    for texto in comentarios:
        try:
            res = sentiment_pipeline(texto[:512])[0]
            score = int(res['label'].split()[0])
            if score >= 4: puntuaciones.append(1)
            elif score <= 2: puntuaciones.append(-1)
            else: puntuaciones.append(0)
        except: continue
    if not puntuaciones: return "Neutro"
    promedio = sum(puntuaciones) / len(puntuaciones)
    return "Positivo" if promedio > 0.2 else "Negativo" if promedio < -0.2 else "Neutro"

def obtener_posts(username, cantidad):
    posts_data = []
    fecha_extraccion = datetime.datetime.now().isoformat()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state="state.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 1. IR AL PERFIL Y HACER SCROLL
            page.goto(f"https://www.instagram.com/{username}/", wait_until="networkidle", timeout=60000)
            
            # Forzamos scroll para cargar más de los 3-4 posts iniciales
            page.mouse.wheel(0, 3000) 
            page.wait_for_timeout(3000) # tiempo para que cargue contenido ms
            
            page.wait_for_selector('a[href*="/p/"]', timeout=15000)
            enlaces = page.query_selector_all('a[href*="/p/"]')
            
            # Usamos un dict para mantener el orden y eliminar duplicados de URLs
            urls = list(dict.fromkeys([f"https://www.instagram.com{e.get_attribute('href')}" for e in enlaces]))[:cantidad]

            for url in urls:
                try:
                    # 2. NAVEGAR AL POST CON MÁS TIEMPO DE CARGA
                    page.goto(url, wait_until="domcontentloaded", timeout=25000)
                    
                    # Espera estratégica para que Instagram cargue los contadores dinámicos
                    page.wait_for_timeout(4000) 

                    # 3. EXTRAER LIKES (Con selector más robusto)
                    likes = "0"
                    # Intentamos esperar a que la sección de interacción sea visible
                    try:
                        likes_elem = page.locator('section').filter(has_text=re.compile(r'likes|me gusta', re.I)).first
                        if likes_elem.is_visible(timeout=5000):
                            txt = likes_elem.inner_text()
                            match = re.search(r'([\d.,\s]+)', txt)
                            if match: 
                                likes = re.sub(r'[.,\s]', '', match.group(1))
                    except:
                        likes = "0"
                    
                    # 4. EXTRAER METADATA Y SENTIMIENTO
                    meta_content = page.locator('meta[property="og:description"]').get_attribute('content') if page.query_selector('meta[property="og:description"]') else ""
                    
                    time_elem = page.query_selector('time')
                    fecha_iso = time_elem.get_attribute('datetime') if time_elem else ""

                    comment_spans = page.query_selector_all('ul li span')
                    comentarios = [s.inner_text() for s in comment_spans if len(s.inner_text()) > 5][:3] # Mantenerte en los 3 primeros evita activar esos sensores.
                    
                    texto_ia = comentarios if comentarios else [meta_content[:500]] #los 500 representan la cantidad de caracteres(letras, espacios y símbolos) que le permites pasar a la IA desde el meta_content
                    sentimiento = analizar_sentimiento_pro(texto_ia)

                    posts_data.append({
                        "url": url,
                        "likes": int(likes) if likes.isdigit() else 0,
                        "fecha": fecha_iso,
                        "hashtags": re.findall(r'#(\w+)', meta_content),
                        "menciones": [f"@{m}" for m in re.findall(r'@(\w+)', meta_content)],
                        "sentimiento": sentimiento
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
            print(f"Error Scraper: {e}")
            return {"fechaExtraccion": fecha_extraccion, "perfil": username, "total": 0, "exitosos": 0, "publicaciones": []}
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
    if not datos_raw: return "No hay datos", 400
    publicaciones = json.loads(datos_raw)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Fecha', 'Likes', 'URL', 'Sentimiento', 'Hashtags', 'Menciones'])
    for p in publicaciones:
        writer.writerow([
            p.get('fecha', '')[:10], 
            p.get('likes'), 
            p.get('url'), 
            p.get('sentimiento'), 
            ", ".join(p.get('hashtags', [])), 
            ", ".join(p.get('menciones', []))
        ])
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=reporte.csv"})

if __name__ == "__main__":
    app.run(debug=True)