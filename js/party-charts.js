$(document).ready(function () {
    $.getJSON("data.json", function (adData) {
        $("#last-updated").text(adData["last_updated"]);
        addPartiesNavBar(adData["party-specific-data"]);

        let searchParams = new URLSearchParams(window.location.search)

        if (!searchParams.has("party")) {
            $('#party-specific-charts').append("<p>No Party Provided.</p>");
            return;
        }

        let party = searchParams.get("party");

        if (!Object.keys(adData["party-specific-data"]).includes(party)) {
            $('#party-specific-charts').append("<p>Party Not Found.</p>");
            return;
        }

        let regionLineChartCanvasId = party.toLowerCase() + "-region-line-chart";
        let regionDoughnutChartCanvasId = party.toLowerCase() + "-region-doughnut-chart";

        let genderLineChartCanvasId = party.toLowerCase() + "-gender-line-chart";
        let genderDoughnutChartCanvasId = party.toLowerCase() + "-gender-doughnut-chart";

        let ageLineChartCanvasId = party.toLowerCase() + "-age-line-chart";
        let ageDoughnutChartCanvasId = party.toLowerCase() + "-age-doughnut-chart";

        let genderAgeLineChartCanvasId = party.toLowerCase() + "-gender-age-line-chart";
        let genderAgeDoughnutChartCanvasId = party.toLowerCase() + "-gender-age-doughnut-chart";

        let partyChartsHTML = `<div id="${party.toLowerCase()}-charts">
            <div class="text-center">
                <h2>${party} Charts</h2>
            </div>
            <div>
                 <div>
                    <div class="text-center">
                        <h3>Impressions per Region (${party})</h3>
                    </div>
                    
                    <div class="row">
                        <div class="col-8">
                            <canvas id="${regionLineChartCanvasId}"></canvas>
                        </div>
                        <div class="col-4">
                            <canvas id="${regionDoughnutChartCanvasId}"></canvas>
                        </div>
                    </div>
                </div>

                <hr>
                <div>
                    <div class="text-center">
                        <h3>Impressions per Gender (${party})</h3>
                    </div>
                    
                    <div class="row">
                        <div class="col-8">
                            <canvas id="${genderLineChartCanvasId}"></canvas>
                        </div>
                        <div class="col-4">
                            <canvas id="${genderDoughnutChartCanvasId}"></canvas>
                        </div>
                    </div>
                </div>
                <hr>

                <div>
                    <div class="text-center">
                        <h3>Impressions per Age (${party})</h3>
                    </div>
                    <div class="row">
                        <div class="col-8">
                            <canvas id="${ageLineChartCanvasId}"></canvas>
                        </div>
                        <div class="col-4">
                            <canvas id="${ageDoughnutChartCanvasId}"></canvas>
                        </div>
                    </div>
                </div>

                <hr>

                <div>
                    <div class="text-center">
                        <h3>Impressions per Gender and Age (${party})</h3>
                    </div>
                    <div class="row">
                        <div class="col-8">
                            <canvas id="${genderAgeLineChartCanvasId}"></canvas>
                        </div>
                        <div class="col-4">
                            <canvas id="${genderAgeDoughnutChartCanvasId}"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <hr>
        </div>`;

        $('#party-specific-charts').append(partyChartsHTML);

        let yAxesPercentage = [{
            ticks: {
                callback: function (value, index, values) {
                    return value + "%";
                }
            }
        }];
        let tooltipsPercentage = {
            mode: 'x',
            intersect: false,
            callbacks: {
                label: function (tooltipItems, data) {
                    return data.datasets[tooltipItems.datasetIndex].label + ": " + tooltipItems.yLabel + "%";
                },

            }
        };

        // Line chart for party impressions per region per day
        let partyRegionLineChart = generateLineGraphConfig(adData,
            "Impressions per Region per Day (" + party + ")",
            "impressions-per-region-per-date",
            party);
        partyRegionLineChart.options.scales.yAxes = yAxesPercentage;
        partyRegionLineChart.options.tooltips = tooltipsPercentage;
        new Chart($("#" + regionLineChartCanvasId), partyRegionLineChart);

        // Doughnut chart for party impressions per region
        let partyRegionDoughnutChart = generateDoughnutChart(adData, "Impressions per Region (" + party + ")", "impressions-per-region", party)
        new Chart($("#" + regionDoughnutChartCanvasId), partyRegionDoughnutChart);


        // Line chart for party impressions per gender per day
        let partyGenderLineChart = generateLineGraphConfig(adData,
            "Impressions per Gender per Day (" + party + ")",
            "impressions-per-gender-per-date",
            party);
        partyGenderLineChart.options.scales.yAxes = yAxesPercentage;
        partyRegionLineChart.options.tooltips = tooltipsPercentage;
        new Chart($("#" + genderLineChartCanvasId), partyGenderLineChart);

        // Doughnut chart for party impressions per gender
        let partyGenderDoughnutChart = generateDoughnutChart(adData, "Impressions per Gender (" + party + ")", "impressions-per-gender", party)
        new Chart($("#" + genderDoughnutChartCanvasId), partyGenderDoughnutChart);


        // Line chart for party impressions per age per day
        let partyAgeLineChart = generateLineGraphConfig(adData,
            "Impressions per Age per Day (" + party + ")",
            "impressions-per-age-per-date",
            party);
        partyAgeLineChart.options.scales.yAxes = yAxesPercentage;
        partyAgeLineChart.options.tooltips = tooltipsPercentage;
        new Chart($("#" + ageLineChartCanvasId), partyAgeLineChart);

        // Doughnut chart for party impressions per age per day
        let partyAgeDoughnutChart = generateDoughnutChart(adData, "Impressions per Age (" + party + ")", "impressions-per-age", party)
        new Chart($("#" + ageDoughnutChartCanvasId), partyAgeDoughnutChart);


        // Party impressions per gender and age per day
        let partyGenderAgeLineChart = generateLineGraphConfig(adData,
            "Impressions per Gender and Age per Day (" + party + ")",
            "impressions-per-gender-and-age-per-date",
            party);
        partyGenderAgeLineChart.options.scales.yAxes = yAxesPercentage;
        partyGenderAgeLineChart.options.tooltips = tooltipsPercentage;
        new Chart($("#" + genderAgeLineChartCanvasId), partyGenderAgeLineChart);

        // Doughnut chart for party impressions per age per day
        let partyGenderAgeDoughnutChart = generateDoughnutChart(adData, "Impressions per Gender and Age(" + party + ")", "impressions-per-gender-and-age", party)
        new Chart($("#" + genderAgeDoughnutChartCanvasId), partyGenderAgeDoughnutChart);
    });
});
