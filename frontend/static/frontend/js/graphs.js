function drawChart(divId, dataList) {
  // debugger
  const element = document.getElementById(divId);
  if (!Array.isArray(dataList) || dataList.length === 0) return;

  const labels = ["Time"];
  const seriesData = [];

  dataList.forEach((data, index) => {
    if (data.labels && data.values) {
      seriesData.push({
        title: data.title || `Serie ${index + 1}`,
        labels: data.labels,
        values: data.values,
      });
    }
  });
  const allDatesSet = new Set(seriesData.flatMap(s => s.labels));
  const allDates = Array.from(allDatesSet).sort((a, b) => new Date(a) - new Date(b));

  const seriesMaps = seriesData.map(s => new Map(s.labels.map((label, i) => [label, s.values[i]])));

  const finalData = allDates.map(date => {
    const row = [new Date(date)];
    seriesMaps.forEach(map => row.push(map.get(date) ?? null));
    return row;
  });

  labels.push(...seriesData.map(s => s.title));
  const colorAttr = element.dataset['color'] || "";
  const customColors = colorAttr.split(';').map(s => s.trim()).filter(Boolean);
  const colors = customColors.length ? customColors : undefined;

  // checkbox container
  const controlId = divId + "-controls";
  let controlContainer = document.getElementById(controlId);
  if (!controlContainer) {
    controlContainer = document.createElement("div");
    controlContainer.id = controlId;
    element.parentNode.insertBefore(controlContainer, element.nextSibling);
  }
  controlContainer.innerHTML = "";

  // visibility tracking
  const visibility = new Array(seriesData.length).fill(true);

  const g = new Dygraph(element, finalData, {
    labels,
    // ylabel: "Metriche",
    animatedZooms: true,
    strokeWidth: 2,
    colors,
    legend: "always",
    labelsUTC: true,
    visibility
  });

  seriesData.forEach((serie, i) => {
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = true;
    checkbox.onchange = () => {
      visibility[i] = checkbox.checked;
      g.updateOptions({ visibility });
    };

    const label = document.createElement("label");
    label.style.marginRight = "20px";
    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(` ${serie.title}`));
    controlContainer.appendChild(label);
  });

  element._dygraphHandle = g;
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

function fetchAndRender(divId) {
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

  // for (let i = 0; i < promises.length; i++){
  //   promises[i].then(dataList => {
  //     console.log("Dati ricevuti:", dataList);
  //     drawChart(divId, dataList);
  //   })
  //     //   .catch(err => {
  // //     console.error("Errore nel caricamento delle metriche:", err);
  // //   });
  // }

  Promise.all(promises)
    .then(dataList => {
      console.log("Dati ricevuti:", dataList);
      drawChart(divId, dataList);
    })
    .catch(err => {
      console.error("Errore nel caricamento delle metriche:", err);
    });
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
});
