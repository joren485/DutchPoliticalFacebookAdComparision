$(document).ready(function () {
    $.getJSON("data.json", function (adData) {
        $("#last-updated").text(adData["last_updated"]);
        addPartiesNavBar(adData["party-specific-data"]);

        // Add active ads line chart
        let activeAdsLineChartConfig = generateLineGraphConfig(adData, "Ads Active per Day", "active-ads-per-date");
        new Chart($("#active-ads-over-time"), activeAdsLineChartConfig);

        // Add total ads doughnut chart
        let totalAdsDoughnutChartConfig = generateDoughnutChart(adData, "Total Ads per Party (" + adData["ads-total"] + " total)", "ads-per-party");
        new Chart($("#ads-per-party"), totalAdsDoughnutChartConfig);

        // Add spending line chart
        let spendingLineChartConfig = generateLineGraphConfig(adData, "Average (Estimated) Spending over Time per Party", "spending-per-date");
        spendingLineChartConfig.options.scales.yAxes = [{
            ticks: {
                callback: function (value, index, values) {
                    return "€" + value.toFixed(2).toString();
                }
            }
        }];

        spendingLineChartConfig.options.tooltips = {
            mode: 'x',
            intersect: false,
            callbacks: {
                label: function (tooltipItems, data) {
                    return data.datasets[tooltipItems.datasetIndex].label + ": €" + tooltipItems.yLabel.toFixed(2).toString();
                }
            }
        };
        new Chart($("#spending-over-time-chart"), spendingLineChartConfig);

        // Add total ads doughnut chart
        let spendingDoughnutChartConfig = generateDoughnutChart(adData, "Total (Estimated) Spending per Party", "spending-per-party");
        spendingDoughnutChartConfig.options.tooltips.callbacks.label = function (tooltipItem, data) {
            return "€" + addPercentageToDoughnutLabel(tooltipItem, data);
        };

        new Chart($("#spending-per-party"), spendingDoughnutChartConfig);
        $("#spending-total-lower").text("€" + adData["spending-total"]["lower"]);
        $("#spending-total-upper").text("€" + adData["spending-total"]["upper"]);

        // Add impressions line chart
        let impressionsLineChartConfig = generateLineGraphConfig(adData, "Average Estimated Impressions per Day", "impressions-data-per-date");
        new Chart($("#impressions-over-time-chart"), impressionsLineChartConfig);

        // Add impressions doughnut chart
        let impressionsDoughnutChartConfig = generateDoughnutChart(adData, "Total (Estimated) Impressions per Party", "impressions-per-party");
        new Chart($("#impressions-per-party"), impressionsDoughnutChartConfig);

        // Add potential reach line chart
        let potentialReachLineChartConfig = generateLineGraphConfig(adData, "Average Potential Reach per Day", "potential-reach-per-date");
        potentialReachLineChartConfig.options.scales.xAxes[0].ticks = {min: new Date("2020-03-31")};
        new Chart($("#potential-reach-chart"), potentialReachLineChartConfig);
        $("#missing-potential-reach").text(adData["ads-without-potential-reach"]);
        $("#total-ads").text(adData["ads-total"]);
    });
});
