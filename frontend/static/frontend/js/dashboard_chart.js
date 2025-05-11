function prepareDygraphData(labels, data1, data2) {
  if (!labels || !data1 || !data2 || labels.length === 0 || data1.length === 0 || data2.length === 0) {
    console.warn("Dati insufficienti per costruire il grafico.");
    return [];
  }

  const combined = [];
  for (let i = 0; i < labels.length; i++) {
    combined.push([new Date(labels[i]), data1[i], data2[i]]);
  }
  return combined;
}

function drawChart(divId, dataList) {
  const element = document.getElementById(divId);
  if (!dataList || dataList.length < 2) {
    console.error("Mancano una o più serie di dati per il grafico.");
    return;
  }

  const [data1, data2] = dataList;

  if (!data1.labels || !data2.labels || data1.labels.length === 0 || data2.labels.length === 0) {
    console.warn("Una delle due serie non contiene etichette.");
    return;
  }

  const labels = data1.labels; // assumiamo che le label siano sincronizzate
  const values1 = data1.values;
  const values2 = data2.values;

  const title1 = data1.title || "Monitor Status";
  const title2 = data2.title || "Is Up";

  if (element._dygraphHandle !== undefined) {
    element._dygraphHandle.destroy();
  }

  const chart_obj = new Dygraph(element, prepareDygraphData(labels, values1, values2), {
    labels: ["Time", title1, title2],
    ylabel: "Status",
    animatedZooms: true,
    strokeWidth: 2,
    colors: ["#007bff", "#28a745"],
    legend: "always",
    labelsUTC: true,
  });

  element._dygraphHandle = chart_obj;
}

function fetchAndRender(divId) {
  const element = document.getElementById(divId);

  Promise.all([
    fetch(`/api/range-data/monitor-status-all?source=endpoint&all=1`).then(res => res.json()),
    fetch(`/api/range-data/is-on-all?source=server&all=1`).then(res => res.json())
  ])
  .then(([endpointData, serverData]) => {
    console.log("Dati ricevuti per endpoint:", endpointData);
    console.log("Dati ricevuti per server:", serverData);
    drawChart(divId, [endpointData, serverData]);
  })
  .catch(err => console.error("Errore nel caricamento delle metriche:", err));
}

function refreshAllCharts() {
  const elements = document.querySelectorAll('.chart');
  for (let i = 0; i < elements.length; i++) {
    fetchAndRender(elements[i].id);
  }
}

function onDataRangeFormSubmit(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const url = form.getAttribute('action') || "";
  const method = form.getAttribute('method') || 'post';

  fetch(url, {
    method: method,
    body: formData,
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  }).then(response => {
    if (response.ok) {
      refreshAllCharts();
    } else if (response.status === 400) {
      response.text().then(text => {
        alert("Errore: " + text);
      });
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const elements = document.querySelectorAll('.chart');
  for (let i = 0; i < elements.length; i++) {
    fetchAndRender(elements[i].id);
  }

  const form = document.getElementById("data-range-form");
  if (form) {
    form.addEventListener('submit', onDataRangeFormSubmit);
  }
});
