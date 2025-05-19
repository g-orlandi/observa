function drawChart(divId, dataList, filter = "both") {
  const element = document.getElementById(divId);
  if (!Array.isArray(dataList) || dataList.length === 0) {
    console.error("No data for charts.");
    return;
  }

  // Raccogli tutte le etichette e i valori in base al filtro
  const allLabels = new Set();
  const allSeries = [];

  dataList.forEach((data, index) => {
    if (!data.labels || !data.values || data.labels.length === 0) {
      console.warn(`Serie ${index} priva di etichette o valori.`);
      return;
    }
    allLabels.add(...data.labels);
    allSeries.push({
      labels: data.labels,
      values: data.values,
      title: data.title || `Serie ${index + 1}`
    });
  });

  if (allSeries.length === 0) {
    console.warn("Nessuna serie valida trovata.");
    return;
  }

  // Elimina eventuale grafico precedente
  if (element._dygraphHandle !== undefined) {
    element._dygraphHandle.destroy();
  }

  // Etichette
const labels = ["Time"];
const colorAttr = element.dataset['color'] || "";
const customColors = colorAttr.split(';').map(c => c.trim()).filter(Boolean);

const activeSeries = allSeries.filter((_, i) => {
  if (filter === "first") return i === 0;
  if (filter === "second") return i === 1;
  return true;
});

labels.push(...activeSeries.map(s => s.title));

const colors = customColors.length > 0
  ? customColors.slice(0, activeSeries.length)
  : ["#007bff", "#28a745", "#ff8800", "#cc00cc", "#00cccc", "#aaaa00"].slice(0, activeSeries.length);

  // Prepara unione temporale dei dati
  const allDatesSet = new Set(activeSeries.flatMap(s => s.labels));
  const allDates = Array.from(allDatesSet).sort((a, b) => new Date(a) - new Date(b));

  const seriesMaps = activeSeries.map(s => new Map(s.labels.map((label, i) => [label, s.values[i]])));

  const finalData = allDates.map(date => {
    const row = [new Date(date)];
    seriesMaps.forEach(map => {
      row.push(map.get(date) ?? null);
    });
    return row;
  });

  const chart_obj = new Dygraph(element, finalData, {
    labels,
    // ylabel: labels.slice(1).join(" / "),
    animatedZooms: true,
    strokeWidth: 2,
    colors: colors.slice(0, activeSeries.length),
    legend: "always",
    labelsUTC: true,
  });

  element._dygraphHandle = chart_obj;
}


function splitBySemicolonColon(str) {
  return str.split(';')
    .map(part => {
      const tokens = part.split(':').map(s => s.trim());
      if (tokens.length !== 3) {
        console.warn("Formato errato in:", part);
        return null;
      }
      return tokens; // [metric, source, all]
    })
    .filter(Boolean);
}

function fetchAndRender(divId, filter = "both") {
  const element = document.getElementById(divId);
  const metricTriples = splitBySemicolonColon(element.dataset['metric']); // [metric, source, all]

  const promises = metricTriples.map(([metric, source, all]) => {
    const allParam = all === "1" || all.toLowerCase() === "true" || all === "all" ? "&all=1" : "";
    const url = `/api/range-data/${metric}?source=${source}${allParam}`;
    return fetch(url).then(res => {
      if (!res.ok) throw new Error(`Errore ${res.status} su ${metric}`);
      return res.json();
    });
  });

  Promise.all(promises)
    .then(dataList => {
      console.log("Dati ricevuti:", dataList);
      drawChart(divId, dataList, filter);
    })
    .catch(err => {
      console.error("Errore nel caricamento delle metriche:", err);
    });
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
