function createGauge(selector, value, label) {
  const options = {
chart: {
  type: 'radialBar',
  height: 350,
  animations: {
    enabled: false 
  }
},

    colors: [value > 0 ? "#28a745" : "#dc3545"],  // green or red
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: {
          background: '#dc3545'  // offline part
        },
        dataLabels: {
          name: { show: false },
          value: {
            fontSize: '24px',
            fontWeight: 'bold',
            offsetY: 10,
            formatter: function (val) {
              return val + '%';
            }
          }
        }
      }
    },
    series: [value],
    labels: [label]
  };

  const chart = new ApexCharts(document.querySelector(selector), options);
  chart.render();
}

function updateDashboard() {
    // Ajax request to django endpoint for get data
  fetch(`/api/online-entities/`)
    .then(res => res.json())
    .then(data => {
      const { entities, servers, endpoints, backups } = data;

      // Arrow function, if total > 0 makes the calc
      const perc = (up, down) => {
        const total = up + down;
        return total > 0 ? Math.round((up / total) * 100) : 0;
      };

      // Destruction ?
      document.querySelector("#gaugeEntities").innerHTML = "";
      document.querySelector("#gaugeServers").innerHTML = "";
      document.querySelector("#gaugeEndpoints").innerHTML = "";
      document.querySelector("#gaugeBackups").innerHTML = "";

      // Gauges
      createGauge("#gaugeEntities", perc(entities.up, entities.down), "Entities");
      createGauge("#gaugeServers", perc(servers.up, servers.down), "Servers");
      createGauge("#gaugeEndpoints", perc(endpoints.up, endpoints.down), "Endpoints");
      createGauge("#gaugeBackups", perc(backups.up, backups.down), "Backups");

      // update text label
      const setText = (id, up, down) => {
        const el = document.getElementById(id);
        el.textContent = `${up}/${up + down} online`;
        el.classList.toggle("text-success", up > 0);
        el.classList.toggle("text-danger", up === 0);
      };

      setText("textEntities", entities.up, entities.down);
      setText("textServers", servers.up, servers.down);
      setText("textEndpoints", endpoints.up, endpoints.down);
      setText("textBackups", backups.up, backups.down);
    })
    .catch(err => console.error('Error while loading data.', err));
}

/** The entire logic for update status of entities, servers and endpoints is done:
 - when the document is loaded
 - every 60 seconds
**/ 
document.addEventListener("DOMContentLoaded", () => {
  updateDashboard();             
  update_interval_in_seconds = 60     
  setInterval(updateDashboard, update_interval_in_seconds * 1000); 
});
