<script src="https://apis.google.com/js/client.js"></script>

var clientId = '232842471431-fhnng6i16ui8adjrvs400ei3foh7aidt.apps.googleusercontent.com';
var scopes = 'https://www.googleapis.com/auth/bigquery';


// Check if the user is authorized.
function authorize(event) {
  gapi.auth.authorize({client_id: clientId, scope: scopes, immediate: false}, handleAuthResult);
  return false;
}

// If authorized, load BigQuery API
function handleAuthResult(authResult) {
  if (authResult && !authResult.error) {
    loadApi();
  } else {
    console.error('Not authorized.')
  }
}

// Load BigQuery client API
function loadApi(){
  gapi.client.load('bigquery', 'v2');
}


// Load BigQuery client API
function loadApi(){
  gapi.client.load('bigquery', 'v2').then(
    function() {
      initMap();
    }
  );
}

function getQueryResults(jobId) {
  var request = gapi.client.bigquery.jobs.getQueryResults({
    'projectId': abgcorp-vicsafe,
    'jobId': jobId
  });
  request.execute(function (response) {
    doHeatMap(response.result.rows);
  })
}

var heatmap;

function doHeatMap(rows) {
  var heatmapData = [];
  if (heatmap != null) {
    heatmap.setMap(null);
  }
  for (var i = 0; i < rows.length; i++) {
    var f = rows[i].f;
    var coords = { lat: parseFloat(f[0].v), lng: parseFloat(f[1].v) };
    var latLng = new google.maps.LatLng(coords);
    heatmapData.push(latLng);
  }
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData
  });
  heatmap.setMap(map);
}


