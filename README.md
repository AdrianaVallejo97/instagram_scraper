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
## 🧪 Entorno Virtual e Instalación

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.

### 🔹 Crear entorno virtual
```bash
python -m venv venv
```
### 🔹 Activar entorno (Windows)
venv\Scripts\activate
### 🔹 Instalar dependencias
pip install -r requirements.txt

### 🔹 Instalar Playwright
playwright install
### 🔐 Manejo de Cookies (Autenticación)

El sistema utiliza cookies para mantener la sesión activa en Instagram y evitar bloqueos.

🔍 ¿Cómo funciona?
Se inicia sesión manualmente en Instagram usando login.py
Playwright guarda la sesión autenticada
Esa sesión se reutiliza en el scraper
📂 ¿Dónde se guardan?
Archivo: state.json
⚙️ ¿Qué contiene?
Cookies de sesión
Tokens de autenticación
Datos de navegación

👉 Esto permite:

Evitar login repetitivo
Simular un usuario real
Reducir detección como bot

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

## 🖥️ Funcionalidades de la Interfaz

La aplicación cuenta con una interfaz web sencilla e intuitiva que permite al usuario interactuar con el sistema de análisis.

### 🔹 Formulario de entrada
- Permite ingresar el **usuario de Instagram**
- Permite definir la **cantidad de publicaciones a analizar**
- Botón **"Analizar"** para iniciar el proceso
- Botón **"Limpiar"** para reiniciar la búsqueda

---

### 🔹 Panel de métricas (cards)
Se muestran indicadores clave:

- 📌 **Posts analizados** → cantidad de publicaciones procesadas  
- ❤️ **Likes promedio** → promedio de interacciones  
- 📅 **Fecha de extracción** → momento del análisis  

---

### 🔹 Tabla de resultados
Presenta la información detallada de cada publicación:

- Fecha de publicación  
- Número de likes  
- Hashtags detectados  
- Menciones encontradas  
- Clasificación de sentimiento  

👉 Incluye:
- Etiquetas visuales (badges) para sentimientos  
- Visualización resumida de hashtags y menciones  

---

### 🔹 Gráfico de sentimientos
- Tipo: **Gráfico de dona (Chart.js)**
- Muestra la distribución de:
  - Positivo  
  - Negativo  
  - Neutro  

👉 Permite identificar rápidamente la percepción general del contenido.

---

### 🔹 Exportación de datos
- Botón **"Exportar CSV"**
- Descarga automática de los resultados
- Incluye:
  - Fecha  
  - Likes  
  - URL  
  - Sentimiento  
  - Hashtags  
  - Menciones  

---

### 🔹 Diseño visual
- Interfaz responsiva (adaptable a distintos dispositivos)
- Uso de **Bootstrap 5**
- Estilo moderno con tarjetas y colores tipo Instagram
- Navegación clara y centrada en el usuario

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
```
## ▶️ Ejecución

Para iniciar la aplicación:

```bash
python app.py
http://127.0.0.1:5000/
```