# AgroPredict IA

AgroPredict IA es una solución fullstack que utiliza Inteligencia Artificial para recomendar cultivos agrícolas a partir de condiciones del suelo y del clima. El proyecto está enfocado en agricultores colombianos, especialmente de Boyacá y Cundinamarca, y permite consultar desde una landing page qué cultivo podría adaptarse mejor a un lote determinado.

El sistema recibe:

- pH del suelo
- Humedad
- Temperatura
- Tipo de suelo

Y retorna una recomendación entre:

- Papa
- Maíz
- Trigo

## Problema o necesidad

Muchos agricultores toman decisiones de siembra con base en experiencia previa, tradición familiar o disponibilidad de semillas, pero no siempre cuentan con herramientas digitales simples que relacionen las condiciones del suelo con el cultivo más conveniente.

La necesidad que busca resolver AgroPredict IA es apoyar la toma de decisiones agrícolas mediante una recomendación automática. La IA no reemplaza el criterio técnico de un agrónomo, pero sí funciona como una primera orientación para identificar qué cultivo puede tener mejor compatibilidad con variables básicas del terreno.

## Solución propuesta

AgroPredict IA combina un modelo de Machine Learning con una interfaz web sencilla. El usuario ingresa los datos del terreno en un formulario, el frontend envía esos datos a una API desarrollada con FastAPI, la API consulta un modelo entrenado con Scikit-learn y devuelve el cultivo recomendado.

Flujo general:

```text
Usuario -> Landing Page -> API FastAPI -> Modelo IA -> Predicción -> Resultado y recomendaciones
```

## Librerías, frameworks y recursos utilizados

Backend:

- `FastAPI`: creación de la API REST.
- `Uvicorn`: servidor ASGI para ejecutar la API localmente.
- `Scikit-learn`: entrenamiento del modelo de Machine Learning.
- `Pandas`: manipulación del dataset.
- `Joblib`: serialización y carga del modelo entrenado.
- `Pydantic`: validación de datos recibidos por la API.

Frontend:

- `HTML5`: estructura de la landing page.
- `CSS3`: diseño responsive, tarjetas visuales y estilos de la interfaz.
- `JavaScript Vanilla`: consumo de la API, validaciones del formulario, estados de carga, errores e historial de predicciones.

Recursos:

- Dataset sintético generado desde reglas agrícolas definidas para papa, maíz y trigo.
- Imagen remota de fondo agrícola usada en la landing page.
- Swagger automático de FastAPI para documentar y probar los endpoints.
- Colección de Postman para consumir la API.

## Construcción del dataset

El dataset se genera automáticamente desde el archivo:

```text
backend/train_model.py
```

El script crea un archivo JSON llamado:

```text
backend/dataset_agricola_colombia.json
```

Cada entrada contiene:

- `ph`
- `humedad`
- `temperatura`
- `tipo_suelo`
- `region`
- `cultivo`

Los cultivos fueron codificados así:

```text
0 = Papa
1 = Maíz
2 = Trigo
```

Los tipos de suelo fueron codificados así:

```text
0 = Arenoso
1 = Arcilloso
2 = Franco
```

Las regiones incluidas fueron:

- Boyacá
- Cundinamarca

### Reglas usadas para generar datos

Papa:

- pH entre 5.0 y 6.2
- Humedad entre 65% y 90%
- Temperatura entre 10°C y 18°C
- Suelo arcilloso o franco

Maíz:

- pH entre 5.8 y 6.8
- Humedad entre 50% y 70%
- Temperatura entre 18°C y 26°C
- Suelo franco

Trigo:

- pH entre 6.0 y 7.5
- Humedad entre 40% y 60%
- Temperatura entre 12°C y 22°C
- Suelo arenoso o franco

Estas reglas permitieron construir datos realistas para un prototipo académico y técnico sin depender de una fuente externa.

## Cantidad de entradas utilizadas

El dataset tiene 1200 registros sintéticos:

- 400 registros para papa
- 400 registros para maíz
- 400 registros para trigo

Para evaluar el modelo se usó una separación de entrenamiento y prueba:

- 80% para entrenamiento
- 20% para prueba

Esto equivale aproximadamente a:

- 960 registros para entrenar
- 240 registros para probar

## Modelo de Machine Learning utilizado

El modelo utilizado fue:

```text
RandomForestClassifier
```

Configuración:

```text
n_estimators = 200
max_depth = 8
class_weight = "balanced"
random_state = 42
```

## Por qué se eligió este modelo

Se eligió `RandomForestClassifier` porque es un modelo robusto para problemas de clasificación con variables numéricas y categóricas codificadas. Además, funciona bien con datasets pequeños o medianos, reduce el riesgo de sobreajuste frente a un solo árbol de decisión y permite capturar relaciones no lineales entre las variables.

Para este caso, el modelo debe clasificar una entrada en una de tres clases posibles: papa, maíz o trigo. Random Forest es una buena opción porque combina múltiples árboles de decisión y entrega una predicción más estable.

## Métricas obtenidas

Durante el entrenamiento se obtuvo una precisión general de prueba de:

```text
Accuracy: 0.9833
```

Reporte por clase:

```text
Clase 0 - Papa
Precision: 1.00
Recall:    1.00
F1-score:  1.00

Clase 1 - Maíz
Precision: 0.95
Recall:    1.00
F1-score:  0.98

Clase 2 - Trigo
Precision: 1.00
Recall:    0.95
F1-score:  0.97
```

La métrica muestra que el modelo logró un desempeño alto con los datos de prueba. Esto se debe a que el dataset fue construido con reglas claras y rangos diferenciados por cultivo. En un escenario productivo, sería recomendable entrenar con datos reales recolectados en campo.

## Predicciones generadas por el sistema

El sistema genera una predicción de cultivo a partir de los datos enviados por el usuario.

Ejemplo de entrada:

```json
{
  "ph": 5.5,
  "humedad": 80,
  "temperatura": 14,
  "tipo_suelo": 1
}
```

Ejemplo de salida:

```json
{
  "cultivo_recomendado": "Papa",
  "codigo_cultivo": 0
}
```

Otros ejemplos:

```text
pH 6.3, humedad 62, temperatura 23, suelo franco -> Maíz
pH 6.8, humedad 48, temperatura 17, suelo arenoso -> Trigo
```

## Uso de las predicciones en la solución

Las predicciones no se muestran únicamente como texto. El frontend aprovecha la respuesta del modelo para construir una experiencia más útil para el usuario.

Cuando la API responde con un cultivo recomendado, la landing page:

- Muestra una tarjeta visual con el cultivo sugerido.
- Agrega la consulta al historial sin borrar resultados anteriores.
- Muestra los valores consultados: pH, humedad, temperatura y tipo de suelo.
- Presenta recomendaciones estáticas asociadas al cultivo predicho.

Esto convierte la predicción del modelo en una orientación práctica para el agricultor.

## Reglas y comportamientos derivados de la predicción

El sistema usa la predicción para activar comportamientos dentro de la interfaz:

- Si el modelo predice `Papa`, se muestran recomendaciones para papa.
- Si el modelo predice `Maíz`, se muestran recomendaciones para maíz.
- Si el modelo predice `Trigo`, se muestran recomendaciones para trigo.
- Cada nueva consulta se agrega como una nueva tarjeta al historial.
- Si hay errores de conexión o datos inválidos, se muestra un mensaje de error amigable.

Estas reglas están implementadas en:

```text
frontend/app.js
```

## Recomendaciones por cultivo

Papa:

- Mantener buena humedad sin encharcar.
- Priorizar suelos sueltos, profundos y con buen drenaje.
- Realizar aporque para proteger tubérculos.
- Monitorear tizón tardío y rotar cultivos.

Maíz:

- Sembrar en suelos francos con buena materia orgánica.
- Garantizar humedad en germinación, floración y llenado de grano.
- Aplicar fertilización balanceada con énfasis en nitrógeno.
- Controlar malezas en etapas tempranas.

Trigo:

- Evitar exceso de humedad.
- Usar semilla de buena calidad.
- Favorecer suelos con drenaje adecuado.
- Monitorear roya y síntomas foliares.

## Cómo se llevó la solución a la web

La solución se llevó a la web mediante una landing page construida con HTML, CSS y JavaScript. No se usaron frameworks frontend para mantener el proyecto simple, liviano y fácil de ejecutar localmente.

La página web consume la API mediante `fetch()`:

```text
POST http://localhost:8000/predict
```

El backend se ejecuta localmente con Uvicorn y expone el endpoint de predicción. El frontend puede abrirse directamente desde el navegador o con una extensión como Live Server.

## Explicación del backend

El backend está ubicado en:

```text
backend/
```

Archivos principales:

- `app.py`: contiene la API FastAPI, el endpoint `/predict`, validaciones con Pydantic, CORS y carga del modelo.
- `train_model.py`: genera el dataset, entrena el modelo y guarda `model.pkl`.
- `dataset_agricola_colombia.json`: dataset generado automáticamente.
- `model.pkl`: modelo entrenado y serializado.
- `requirements.txt`: dependencias necesarias.

Endpoint principal:

```text
POST /predict
```

La API también cuenta con documentación automática en:

```text
http://localhost:8000/docs
```

## Explicación del frontend

El frontend está ubicado en:

```text
frontend/
```

Archivos principales:

- `index.html`: estructura de la landing page, formulario, historial y recomendaciones.
- `style.css`: diseño visual, responsive layout, tarjetas y estados.
- `app.js`: validaciones, consumo de la API, renderizado de resultados y manejo de errores.

La interfaz tiene como objetivo permitir que cualquier usuario ingrese condiciones básicas del terreno y reciba una recomendación clara. Además, conserva el historial de consultas para comparar diferentes escenarios de suelo.

## Estructura del proyecto

```text
agropredict-ia/
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── model.pkl
│   ├── requirements.txt
│   └── dataset_agricola_colombia.json
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── postman/
│   └── AgroPredictIA.postman_collection.json
├── .gitignore
└── README.md
```

## Instalación

Desde la carpeta del backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Entrenar el modelo

El script genera automáticamente el dataset y entrena el modelo:

```bash
cd backend
python train_model.py
```

Al finalizar se crean o actualizan:

```text
dataset_agricola_colombia.json
model.pkl
```

## Ejecutar backend

```bash
cd backend
uvicorn app:app --reload
```

La API queda disponible en:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

## Ejecutar frontend

Abrir el archivo:

```text
frontend/index.html
```

También se puede usar Live Server desde el editor.

## Probar con Postman

El proyecto incluye una colección de Postman en:

```text
postman/AgroPredictIA.postman_collection.json
```

La variable base es:

```text
base_url = http://localhost:8000
```

## Licencia sugerida

Para este tipo de proyecto académico y prototipo tecnológico se recomienda usar licencia MIT, ya que permite reutilizar, modificar y compartir el código con pocas restricciones.
