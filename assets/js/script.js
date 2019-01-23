// App initialization code goes here
function loadChart() 
{
    // Load google charts
    google.charts.load('current', {
        'packages': ['corechart']
    });
    google.charts.setOnLoadCallback(drawChart);

    // Draw the chart and set the chart values
    function drawChart() {
        var data = google.visualization.arrayToDataTable([
                ['Task', 'Hours per Day'],
                ['Work', 10],
                ['Eat', 2],
                ['TV', 4],
                ['Gym', 2],
                ['Sleep', 8]
                ]);

        // Optional; add a title and set the width and height of the chart
        var options = {
            'width': 300,
            'height': 200,
            legend: {
                position: 'none'
            },
            backgroundColor: "aliceblue"
        };

        // Display the chart inside the <div> element with id="piechart"
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
    }
}

function loadCrimes() 
{
    document.getElementById("crime1").innerHTML = "1st: spitting out gum";
    document.getElementById("crime2").innerHTML = "2nd: stepping on grass they should not have";
    document.getElementById("crime3").innerHTML = "3rd: spitting out gum";
}


function updatePage() 
{
    loadCrimes();
    loadChart();
}
window.onload = updatePage;
