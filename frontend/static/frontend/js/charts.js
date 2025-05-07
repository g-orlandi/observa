function prepareDygraphData(labels, dataSeries) {
  return labels.map((label, i) => [new Date(label), dataSeries[i]]);
}

function drawChart(divId, labels, values, ylabel, color) {
  new Dygraph(document.getElementById(divId), prepareDygraphData(labels, values), {
    labels: ["Time", ylabel],
    ylabel: ylabel,
    animatedZooms: true,
    strokeWidth: 2,
    colors: [color],
    legend: "always",
    labelsUTC: true,
  });
}

function fetchAndRender(metric, divId, ylabel, color) {
  fetch(`/api/range-data/${metric}/`)
    .then(res => res.json())
    .then(data => {
      drawChart(divId, data.labels, data.values, ylabel, color);
    })
    .catch(err => console.error(`Errore nel caricamento dati per ${metric}:`, err));
}

document.addEventListener("DOMContentLoaded", () => {
  fetchAndRender("cpu-usage", "cpuChart", "CPU (%)", "#0d6efd");
  fetchAndRender("mem-used", "memoryChart", "Memory Used (GB)", "#6610f2");
  fetchAndRender("disk-used", "diskChart", "Disk Used (GB)", "#6610a2");
});
