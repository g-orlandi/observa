function prepareDygraphData(labels, dataSeries) {
  return labels.map((label, i) => [new Date(label), dataSeries[i]]);
}

function drawChart(divId, data) {
  element = document.getElementById(divId);
  color = element.dataset['color'];
  title = data.title;

  if(element._dygraphHandle !== undefined){
    // If we have already created an object, we destroy it to avoid memory leaks
    element._dygraphHandle.destroy();
  }
  chart_obj = new Dygraph(document.getElementById(divId), prepareDygraphData(data.labels, data.values), {
    labels: ["Time", title],
    ylabel: title,
    animatedZooms: true,
    strokeWidth: 2,
    colors: [color],
    legend: "always",
    labelsUTC: true,
  });

  // We save the dygraph object in a property of the element in order to retrieve it later on
  element._dygraphHandle = chart_obj; 
}

function fetchAndRender(divId) {
  element = document.getElementById(divId);
  metric = element.dataset['metric'];
  pathname = window.location.pathname;
  if (pathname === '/network/'){
    source = 'endpoint';
  }
  else if(pathname === '/resources/'){
    source = 'server';
  }
  fetch(`/api/range-data/${metric}?source=${source}`)
    .then(res => res.json())
    .then(data => {   
      drawChart(divId, data);
    })
    .catch(err => console.error(`Errore nel caricamento dati per ${metric}:`, err));
}

document.addEventListener("DOMContentLoaded", () => {
  elements = document.querySelectorAll('.chart');
  console.log(elements)
  for (i = 0; i < elements.length; i++){
    fetchAndRender(elements[i].id);
  };

  // Intercettiamo l'evento submit perche' vogliamo gestirlo via js per evitare di ricaricare l'intera pagina
  let form = document.getElementById("data-range-form");
  form.addEventListener('submit', onDataRangeFormSubmit);
});

function onDataRangeFormSubmit(event){
  event.preventDefault();
  console.log('Submit');

  let form = event.target;
  let formData = new FormData(form);
  let url = form.getAttribute('action') || "";
  let method = form.getAttribute('method') || 'post';
  // Convert formData into a plain object
  data = Object.fromEntries(formData.entries());

  console.log('form data: %o', formData);
  console.log('form data: %o', new URLSearchParams(formData).toString());
  console.log('data: %o', data)

  fetch(
    url, {
        method: method,
        body: formData,
        // TO-DO verificare che fanno
        mode: 'cors',   // 'no-cors', 
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            // make sure request.is_ajax() return True on the server
            'X-Requested-With': 'XMLHttpRequest'
        }
    }
  ).then(response => {
    if(response.ok){
    refreshAllCharts()
    }
    else if (response.status === 400){
      response.text().then(text => {
        alert("Error: " + text);
      })
    }
  }
  );
}



function refreshAllCharts(){
  elements = document.querySelectorAll('.chart');
  console.log(elements)
  for (i = 0; i < elements.length; i++){
    fetchAndRender(elements[i].id);
  };
}
