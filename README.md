# 📊 Instagram Analytics Pro

🔗 **Repositorio:**  
👉 https://github.com/AdrianaVallejo97/instagram_scraper

---

## 🚀 Descripción

Aplicación web desarrollada con Flask que permite analizar perfiles de Instagram mediante scraping automatizado, procesamiento de datos y análisis de sentimiento con inteligencia artificial.

---

## 🧠 Inteligencia Artificial

**Modelo utilizado:**

`nlptown/bert-base-multilingual-uncased-sentiment`

### 🔍 Características
- Basado en arquitectura BERT
- Multilenguaje (incluye español)
- Clasificación de sentimientos en escala de 1 a 5

### 📊 Interpretación

- ⭐ 1–2 → Negativo  
- ⭐ 3 → Neutro  
- ⭐ 4–5 → Positivo  

Se promedia el resultado para obtener el sentimiento final del post.

---

## ⚙️ Tecnologías

### 🔹 Backend
- Python
- Flask
- Playwright (scraping automatizado)
- Transformers (NLP)


### 🔹 Frontend
- HTML5
- CSS3
- Bootstrap 5
- Chart.js
- JavaScript

---

## ⚙️ Funcionamiento del Scraper

El sistema usa automatización con navegador real (Playwright), lo cual es clave porque:

- Instagram detecta bots fácilmente  
- Los datos se cargan dinámicamente (JavaScript)  
- Se necesita simular comportamiento humano  

---

## ⏱️ Lógica de tiempos

- `page.goto()` → 60000 ms  
- Scroll → 3000 ms  
- Espera del post → 4000 ms  
- Selector → 15000 ms  

Esto evita bloqueos y asegura datos completos.

---

## 📉 Límite de publicaciones

- Mínimo: 1  
- Máximo: 20  

**Razón:**
- Evitar bloqueos  
- Mejorar rendimiento  
- Reducir carga del modelo IA  

---

## 📊 Dashboard

Incluye:

- ✔ Total de posts analizados  
- ✔ Promedio de likes  
- ✔ Fecha de extracción  
- ✔ Tabla con datos  
- ✔ Gráfico de sentimientos  

---

## 📁 Estructura del Proyecto

```bash
INSTAGRAM_SCRAPER/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── dashboard.js
│
├── templates/
│   ├── index.html
│   └── _results.html
│
├── app.py
├── login.py
├── requirements.txt
├── state.json
└── README.md

---
## ▶️ Ejecución

```bash
python app.py

Abrir en:

http://127.0.0.1:5000/
📤 Exportación

Formato CSV con:

Fecha
Likes
URL
Sentimiento
Hashtags
Menciones
👩‍💻 Autora

Adriana Thalia Vallejo Muñoz
Ingeniería en Sistemas