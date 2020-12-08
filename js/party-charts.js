$(document).ready(function () {
    $.getJSON("data.json", function (adData) {
        let searchParams = new URLSearchParams(window.location.search)

        if (!searchParams.has("party")) {
            $("#party-specific-charts").append("<p>No Party Provided.</p>");
            return;
        }

        let party = searchParams.get("party");

        if (!Object.keys(adData["party-specific-data"]).includes(party)) {
            $("#party-specific-charts").append("<p>Party Not Found.</p>");
            return;
        }

        console.log(adData['party-specific-data'][party]['ads-per-party']);

        $("#party-specific-charts").append(
            `<div class="text-center">
                <h3>${party} Graphs</h3>
                <p class="lead">${party} ran ${adData['party-specific-data'][party]['ads-per-party']} ads and spent an estimated €${adData['party-specific-data'][party]['spending-per-party'].toFixed(2)}.</p>
            </div>
            <hr>`);

        let partySpecificCharts = [
            {"labelType": "Region", "dataType": "Spending"},
            {"labelType": "Gender", "dataType": "Spending"},
            {"labelType": "Age", "dataType": "Spending"},
        ];

        partySpecificCharts.forEach(function (element){

            let labelType = element["labelType"];
            let dataType = element["dataType"];

            let LineChartCanvasId = party.toLowerCase() + "-" + labelType.toLowerCase() + "-" + dataType.toLowerCase() + "-line-chart";
            let DoughnutChartCanvasId = party.toLowerCase()+ "-" + labelType.toLowerCase() + "-" + dataType.toLowerCase() +  "-doughnut-chart";

            $("#party-specific-charts").append(
                `<div>
                    <div class="text-center">
                        <h3>Estimated ${dataType} per ${labelType} (${party})</h3>
                    </div>
                    
                    <div class="row">
                        <div class="col-8">
                            <canvas id="${LineChartCanvasId}"></canvas>
                            <p>This graph shows how much each party spent per ${labelType.toLowerCase()} on ads over time. Facebook provides a range (e.g. €1000 - €1999 has been spent on an ad) for each ad, this graph is based on the average of the range of each ad.</p>
                        </div>
                        <div class="col-4">
                            <canvas id="${DoughnutChartCanvasId}"></canvas>
                        </div>
                    </div>
                </div>
                <hr>`);


            let lineChart = generateLineGraphConfig(adData,
                "Estimated " + dataType + " per " + labelType + " per Day ("+ party + ")",
                dataType.toLowerCase() + "-per-" + labelType.toLowerCase() + "-per-date",
                party);

            lineChart.options.scales.yAxes = [{
                ticks: {
                    callback: function (value, index, values) {
                        return "€" + value;
                    }
                }
            }];
            lineChart.options.tooltips = {
                mode: "x",
                intersect: false,
                callbacks: {
                    label: function (tooltipItems, data) {
                        return data.datasets[tooltipItems.datasetIndex].label + ": €" + tooltipItems.yLabel;
                    },

                }
            };
            new Chart($("#" + LineChartCanvasId), lineChart);

            let doughnutChart = generateDoughnutChart(adData,
                "Estimated " + dataType + " per " + labelType + " (" + party + ")",
                dataType.toLowerCase() + "-per-" + labelType.toLowerCase(),
                party)
            new Chart($("#" + DoughnutChartCanvasId), doughnutChart);
        });

    });
});
