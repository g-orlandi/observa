function renderCharts(cpu, mem, labels) {
    console.log('here2');
    const cpuCanvas = document.getElementById("cpuChart");
    const memCanvas = document.getElementById("memoryChart");
  
    const existingCpuChart = Chart.getChart(cpuCanvas);
    if (existingCpuChart) existingCpuChart.destroy();
  
    const existingMemChart = Chart.getChart(memCanvas);
    if (existingMemChart) existingMemChart.destroy();
  
    const commonOptions = {
      type: 'line',
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        scales: {
          y: { beginAtZero: true }
        }
      }
    };
  
    new Chart(cpuCanvas, {
      ...commonOptions,
      data: {
        labels,
        datasets: [{
          label: "CPU (%)",
          data: cpu,
          borderWidth: 2
        }]
      }
    });
  
    new Chart(memCanvas, {
      ...commonOptions,
      data: {
        labels,
        datasets: [{
          label: "Memory Used (GB)",
          data: mem,
          borderWidth: 2
        }]
      }
    });
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    const raw = document.getElementById("graph-data");
    if (raw) {
      try {
        const { cpu, memory, labels } = JSON.parse(raw.textContent);
        renderCharts(cpu, memory, labels);
      } catch (err) {
        console.warn("Errore JSON init:", err);
      }
    }
  });
  
//   document.body.addEventListener("htmx:afterSwap", function (e) {
//     if (e.detail.target.id === "graphs-container") {
//       const raw = document.getElementById("graph-data");
//       if (!raw) return;
  
//       try {
//         const { cpu, memory, labels } = JSON.parse(raw.textContent);
//         renderCharts(cpu, memory, labels);
//       } catch (err) {
//         console.warn("Errore JSON HTMX:", err);
//       }
//     }
//   });
  