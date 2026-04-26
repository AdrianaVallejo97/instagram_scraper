📊 Instagram Analytics Pro

🔗 Repositorio:
👉 https://github.com/AdrianaVallejo97/instagram_scraper

🚀 Descripción

Aplicación web desarrollada con Flask que permite analizar perfiles de Instagram mediante scraping automatizado, procesamiento de datos y análisis de sentimiento con inteligencia artificial.

🧠 Inteligencia Artificial

Modelo utilizado:

nlptown/bert-base-multilingual-uncased-sentiment
🔍 Características
Basado en arquitectura BERT
Multilenguaje (incluye español)
Clasificación de sentimientos en escala de 1 a 5
📊 Interpretación:
Estrellas	Resultado
1–2 ⭐	Negativo
3 ⭐	Neutro
4–5 ⭐	Positivo

Se promedia el resultado para obtener el sentimiento final del post.

⚙️ Tecnologías
🔹 Backend
Python
Flask
Playwright (scraping automatizado)
Transformers (NLP)
PyTorch
🔹 Frontend
HTML5
CSS3
Bootstrap 5
Chart.js
JavaScript
⚙️ Funcionamiento del Scraper

Tu sistema usa automatización con navegador real (Playwright), lo cual es clave porque:

Instagram detecta bots fácilmente
Los datos se cargan dinámicamente (JavaScript)
Se necesita simular comportamiento humano

👉 En comunidades de desarrollo se menciona que muchos scrapers usan navegadores automatizados (como Selenium o Playwright), pero esto puede ser más lento y complejo frente a APIs directas

⏱️ Lógica de tiempos (anti-bloqueo)
Acción	Tiempo	Motivo
page.goto()	60000 ms	Carga completa del perfil
Scroll	3000 ms	Cargar más posts
Espera post	4000 ms	Render dinámico
Selector	15000 ms	Evitar errores

💡 Estos tiempos evitan:

Bloqueos de Instagram
Datos incompletos
Detección como bot
📉 Límite de publicaciones
Mínimo: 1
Máximo: 20
🎯 Justificación:
Reduce riesgo de bloqueo
Optimiza rendimiento del modelo IA
Mejora tiempos de respuesta
📊 Dashboard

Incluye:

✔ Total de posts analizados
✔ Promedio de likes
✔ Fecha de extracción
✔ Tabla con datos
✔ Gráfico de sentimientos (Chart.js)
📁 Estructura del Proyecto
INSTAGRAM_SCRAPER/
│
├── static/
│   ├── css/style.css
│   ├── js/dashboard.js
│
├── templates/
│   ├── index.html
│   ├── _results.html
│
├── app.py
├── login.py
├── requirements.txt
├── state.json
└── README.md
📥 Instalación
git clone https://github.com/AdrianaVallejo97/instagram_scraper.git
cd instagram_scraper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install
🔑 Login
python login.py
Inicia sesión en Instagram
Presiona ENTER
Se genera state.json
▶️ Ejecución
python app.py

Abrir en:

http://127.0.0.1:5000/
📤 Exportación

Formato disponible:

CSV

Incluye:

Fecha
Likes
URL
Sentimiento
Hashtags
Menciones
⚠️ Consideraciones
Instagram cambia constantemente su estructura
Scraping puede fallar si hay cambios en el DOM
Uso recomendado: educativo / investigación
📈 Mejoras Futuras
API REST
Base de datos (MongoDB / PostgreSQL)
NLP más avanzado
Dashboard con filtros
Deploy en la nube (AWS / Render)
👩‍💻 Autora

Adriana Thalia Vallejo Muñoz
Ingeniería en Sistemas