function getQueryResults(jobId){
  var request = gapi.client.bigquery.jobs.getQueryResults({
    'projectId': billingProjectId,
    'jobId': jobId
  });
  request.execute(function(response){
    doHeatMap(response.result.rows);
  })
}

var heatmap;

function doHeatMap(rows){
  var heatmapData = [];
  if (heatmap!=null){
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