function prepareDygraphData(labels1, data1, labels2, data2, filter = "both") {
  if (!labels1 || !data1 || !labels2 || !data2) {
    console.warn("Dati insufficienti per costruire il grafico.");
    return [];
  }

  const allDatesSet = new Set([...labels1, ...labels2]);
  const allDates = Array.from(allDatesSet).sort((a, b) => new Date(a) - new Date(b));

  const map1 = new Map(labels1.map((label, idx) => [label, data1[idx]]));
  const map2 = new Map(labels2.map((label, idx) => [label, data2[idx]]));

  return allDates.map(date => {
    const row = [new Date(date)];
    if (filter === "first") {
      row.push(map1.has(date) ? map1.get(date) : null);
    } else if (filter === "second") {
      row.push(map2.has(date) ? map2.get(date) : null);
    } else {
      row.push(map1.has(date) ? map1.get(date) : null);
      row.push(map2.has(date) ? map2.get(date) : null);
    }
    return row;
  });
}

function drawChart(divId, dataList, filter = "both") {
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

  const values1 = data1.values;
  const values2 = data2.values;

  const title1 = data1.title || "Monitor Status";
  const title2 = data2.title || "Is Up";

  if (element._dygraphHandle !== undefined) {
    element._dygraphHandle.destroy();
  }

  const labels = ["Time"];
  if (filter === "first") labels.push(title1);
  else if (filter === "second") labels.push(title2);
  else labels.push(title1, title2);

  const chart_obj = new Dygraph(
    element,
    prepareDygraphData(data1.labels, values1, data2.labels, values2, filter),
    {
      labels: labels,
      ylabel: "Status",
      animatedZooms: true,
      strokeWidth: 2,
      colors: ["#007bff", "#28a745"],
      legend: "always",
      labelsUTC: true,
    }
  );

  element._dygraphHandle = chart_obj;
}

function fetchAndRender(divId, filter = "both") {
  const element = document.getElementById(divId);

  Promise.all([
    fetch(`/api/range-data/monitor-status-all?source=endpoint&all=1`).then(res => res.json()),
    fetch(`/api/range-data/is-on-all?source=server&all=1`).then(res => res.json())
  ])
  .then(([endpointData, serverData]) => {
    console.log("Dati ricevuti per endpoint:", endpointData);
    console.log("Dati ricevuti per server:", serverData);
    drawChart(divId, [endpointData, serverData], filter);
  })
  .catch(err => console.error("Errore nel caricamento delle metriche:", err));
}

function refreshAllCharts(filter = "both") {
  const elements = document.querySelectorAll('.chart');
  for (let i = 0; i < elements.length; i++) {
    fetchAndRender(elements[i].id, filter);
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
      const selectedFilter = document.getElementById("seriesSelector")?.value || "both";
      refreshAllCharts(selectedFilter);
    } else if (response.status === 400) {
      response.text().then(text => {
        alert("Errore: " + text);
      });
    } else {
      console.error("Errore nella richiesta:", response.status);
    }
  }).catch(error => {
    console.error("Errore durante il fetch:", error);
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

  const selector = document.getElementById("seriesSelector");
  if (selector) {
    selector.addEventListener("change", () => {
      const selected = selector.value;
      refreshAllCharts(selected);
    });
  }
});
