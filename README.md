# Instagram Scraper
Aplicación web desarrollada con Flask que permite obtener información de publicaciones públicas de Instagram, visualizar métricas y realizar análisis básico de sentimientos.

---
## Características

* Búsqueda de perfiles públicos de Instagram
* Extracción de publicaciones (likes, comentarios)
* Análisis de sentimientos en comentarios
* Visualización con gráficos (Chart.js)
* Interfaz moderna con Bootstrap
* Exportación de datos (CSV, Excel, PDF)

---

## Tecnologías utilizadas

* Python
* Flask
* Requests
* Pandas
* TextBlob (NLP)
* Bootstrap
* Chart.js

---

## Estructura del proyecto

```
instagram_scraper/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
```

---

## Instalación

1. Clonar repositorio:

```
git clone https://github.com/TU-USUARIO/instagram_scraper.git
cd instagram_scraper
```

2. Crear entorno virtual:

```
python -m venv venv
```

3. Activar entorno:

Windows:

```
venv\Scripts\activate
```

4. Instalar dependencias:

```
pip install -r requirements.txt
```

---

## Ejecución

```
python app.py
```

Abrir en navegador:

```
http://127.0.0.1:5000/
```

---

## Funcionalidades

* Ingresar nombre de usuario
* Seleccionar cantidad de publicaciones
* Visualizar métricas de engagement
* Analizar sentimientos de comentarios
* Exportar resultados en múltiples formatos

---

## Limitaciones

* Solo funciona con perfiles públicos
* Instagram puede bloquear requests automáticos
* El análisis de sentimientos es básico
* No se obtiene información de reposts

---

##  Autor

Proyecto desarrollado por estudiante de Ingeniería en Sistemas como práctica de scraping, análisis de datos y desarrollo web.

---

## Recomendación

Este proyecto puede extenderse con:

* Uso de APIs oficiales
* Modelos NLP más avanzados
* Dashboard tipo Power BI
* Despliegue en la nube

---
