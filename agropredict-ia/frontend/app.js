const API_URL = "http://localhost:8000/predict";

const form = document.querySelector("#predictionForm");
const submitButton = document.querySelector("#submitButton");
const formMessage = document.querySelector("#formMessage");
const resultHistory = document.querySelector("#resultHistory");
const resultsList = document.querySelector("#resultsList");
const recommendationPanels = document.querySelectorAll(".recommendation-panel");

const cropMessages = {
  Papa: "La papa suele responder bien a suelos frescos, con buena humedad y condiciones de montaña.",
  Maíz: "El maíz puede aprovechar temperaturas más cálidas y suelos francos con humedad moderada.",
  Trigo: "El trigo se adapta a condiciones templadas y suelos con humedad controlada.",
};

const soilTypes = {
  0: "Arenoso",
  1: "Arcilloso",
  2: "Franco",
};

function setMessage(message, type = "info") {
  formMessage.textContent = message;
  formMessage.classList.toggle("error", type === "error");
}

function getPayload() {
  return {
    ph: Number(document.querySelector("#ph").value),
    humedad: Number(document.querySelector("#humedad").value),
    temperatura: Number(document.querySelector("#temperatura").value),
    tipo_suelo: Number(document.querySelector("#tipo_suelo").value),
  };
}

function validatePayload(payload) {
  if (Number.isNaN(payload.ph) || payload.ph < 0 || payload.ph > 14) {
    return "Ingresa un pH entre 0 y 14.";
  }

  if (Number.isNaN(payload.humedad) || payload.humedad < 0 || payload.humedad > 100) {
    return "Ingresa una humedad entre 0% y 100%.";
  }

  if (
    Number.isNaN(payload.temperatura) ||
    payload.temperatura < -20 ||
    payload.temperatura > 60
  ) {
    return "Ingresa una temperatura válida entre -20°C y 60°C.";
  }

  if (![0, 1, 2].includes(payload.tipo_suelo)) {
    return "Selecciona un tipo de suelo válido.";
  }

  return "";
}

function getRecommendations(cropName) {
  const panel = Array.from(recommendationPanels).find(
    (recommendationPanel) => recommendationPanel.dataset.crop === cropName,
  );

  if (!panel) {
    return "";
  }

  const clonedPanel = panel.cloneNode(true);
  clonedPanel.classList.remove("hidden");
  return clonedPanel.outerHTML;
}

function renderResult(data, payload) {
  const cropDescription =
    cropMessages[data.cultivo_recomendado] ||
    "Este cultivo se adapta bien a las condiciones ingresadas.";
  const resultItem = document.createElement("article");

  resultItem.className = "result-card";
  resultItem.innerHTML = `
    <p class="result-label">Cultivo recomendado</p>
    <h3>${data.cultivo_recomendado}</h3>
    <p>${cropDescription}</p>
    <dl class="result-meta">
      <div>
        <dt>pH</dt>
        <dd>${payload.ph}</dd>
      </div>
      <div>
        <dt>Humedad</dt>
        <dd>${payload.humedad}%</dd>
      </div>
      <div>
        <dt>Temperatura</dt>
        <dd>${payload.temperatura}°C</dd>
      </div>
      <div>
        <dt>Suelo</dt>
        <dd>${soilTypes[payload.tipo_suelo]}</dd>
      </div>
    </dl>
    <div class="crop-recommendations">
      ${getRecommendations(data.cultivo_recomendado)}
    </div>
  `;

  resultsList.prepend(resultItem);
  resultHistory.classList.remove("hidden");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = getPayload();
  const validationError = validatePayload(payload);

  if (validationError) {
    setMessage(validationError, "error");
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Analizando suelo...";
  setMessage("Consultando el modelo de AgroPredict IA...");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("La API no respondió correctamente.");
    }

    const data = await response.json();
    renderResult(data, payload);
    setMessage("Predicción generada correctamente.");
  } catch (error) {
    setMessage(
      "No se pudo conectar con la API. Verifica que el backend esté corriendo en http://localhost:8000.",
      "error",
    );
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Recomendar cultivo";
  }
});
