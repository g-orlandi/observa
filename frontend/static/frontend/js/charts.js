// Funzione per preparare i dati nel formato Dygraphs
function prepareDygraphData(labels, dataSeries) {
  return labels.map((label, i) => {
    return [new Date(label), dataSeries[i]];
  });
}

// Funzione per renderizzare i grafici CPU e Memoria
function renderCharts(cpu, mem, disk, labels) {
  const cpuDiv = document.getElementById("cpuChart");
  const memDiv = document.getElementById("memoryChart");
  const diskDiv = document.getElementById("diskChart");

  const cpuData = prepareDygraphData(labels, cpu);
  const memData = prepareDygraphData(labels, mem);
  const diskData = prepareDygraphData(labels, disk)

  new Dygraph(cpuDiv, cpuData, {
    labels: ["Time", "CPU (%)"],
    ylabel: "CPU (%)",
    animatedZooms: true,
    strokeWidth: 2,
    colors: ["#0d6efd"],
    legend: "always",
    labelsUTC: true,
  });

  new Dygraph(memDiv, memData, {
    labels: ["Time", "Memory (GB)"],
    ylabel: "Memory Used (GB)",
    animatedZooms: true,
    strokeWidth: 2,
    colors: ["#6610f2"],
    legend: "always",
    labelsUTC: true,
  });

  new Dygraph(diskDiv, diskData, {
    labels: ["Time", "Disk (GB)"],
    ylabel: "Disk Used (GB)",
    animatedZooms: true,
    strokeWidth: 2,
    colors: ["#6610a2"],
    legend: "always",
    labelsUTC: true,
  });
}

// Inizializza i grafici al caricamento della pagina
document.addEventListener("DOMContentLoaded", () => {
  const raw = document.getElementById("graph-data");
  if (raw) {
    try {
      const { cpu, memory, disk, labels } = JSON.parse(raw.textContent);
      renderCharts(cpu, memory, disk, labels);
    } catch (err) {
      console.warn("Errore JSON init:", err);
    }
  }
});

// Ricarica i grafici dopo HTMX swap (es. cambio intervallo)
document.body.addEventListener("htmx:afterSwap", function (e) {
  if (e.detail.target.id === "graphs-container") {
    const raw = document.getElementById("graph-data");
    if (!raw) return;

    try {
      const { cpu, memory, disk, labels } = JSON.parse(raw.textContent);
      renderCharts(cpu, memory, disk, labels);
    } catch (err) {
      console.warn("Errore JSON HTMX:", err);
    }
  }
});
