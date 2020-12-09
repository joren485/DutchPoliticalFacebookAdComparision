$(document).ready(function () {
    $.getJSON("data.json", function (adData) {

        // Add active ads line chart
        let activeAdsLineChartConfig = generateLineGraphConfig(adData, "Ads Active over time", "active-ads-per-date");
        new Chart($("#active-ads-over-time"), activeAdsLineChartConfig);
        $(".total-ads").text(adData["ads-total"]);

        // Add total ads doughnut chart
        let totalAdsDoughnutChartConfig = generateDoughnutChart(adData, "Total Ads", "ads-per-party");
        new Chart($("#ads-per-party"), totalAdsDoughnutChartConfig);

        // Add spending line chart
        let spendingLineChartConfig = generateLineGraphConfig(adData, "Average (Estimated) Spending over time", "spending-per-date");
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
        let spendingDoughnutChartConfig = generateDoughnutChart(adData, "Total (Estimated) Spending", "spending-per-party");
        spendingDoughnutChartConfig.options.tooltips.callbacks.label = function (tooltipItem, data) {
            return "€" + addPercentageToDoughnutLabel(tooltipItem, data);
        };

        new Chart($("#spending-per-party"), spendingDoughnutChartConfig);
        $("#spending-total-lower").text("€" + adData["spending-total"]["lower"]);
        $("#spending-total-upper").text("€" + adData["spending-total"]["upper"]);

        $("#most-expensive-ad-cost").text("€" + adData["most-expensive-ad"]["cost"].toFixed(2));
        $("#most-expensive-ad-party").text(adData["most-expensive-ad"]["party"]);
        $("#most-expensive-ad-days").text(adData["most-expensive-ad"]["days"]);

        $("#most-expensive-ad-link").attr("href", $("#most-expensive-ad-link").attr("href") + adData["most-expensive-ad"]["id"]);

        // Add impressions line chart
        let impressionsLineChartConfig = generateLineGraphConfig(adData, "Average (Estimated) Impressions over time", "impressions-data-per-date");
        new Chart($("#impressions-over-time-chart"), impressionsLineChartConfig);

        // Add impressions doughnut chart
        let impressionsDoughnutChartConfig = generateDoughnutChart(adData, "Total (Estimated) Impressions", "impressions-per-party");
        new Chart($("#impressions-per-party"), impressionsDoughnutChartConfig);

        // Add potential reach line chart
        let potentialReachLineChartConfig = generateLineGraphConfig(adData, "Average Potential Reach over time", "potential-reach-per-date");
        potentialReachLineChartConfig.options.scales.xAxes[0].ticks = {min: new Date("2020-03-31")};
        new Chart($("#potential-reach-chart"), potentialReachLineChartConfig);
        $("#missing-potential-reach").text(adData["ads-without-potential-reach"]);
    });
});
