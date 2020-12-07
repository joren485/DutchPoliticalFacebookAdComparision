$(document).ready(function () {
    $.getJSON("data.json", function (adData) {
        $("#last-updated").text(adData["last_updated"]);

        // Add active ads line chart
        let activeAdsLineChartConfig = generateLineGraphConfig(adData, "Ads Active per Day", "active_ads");
        new Chart($("#active-ads-over-time"), activeAdsLineChartConfig);

        // Add total ads doughnut chart
        let totalAdsDoughnutChartConfig = generateDoughnutChart(adData, "Total Ads per Party (" + adData["total_ads"] + " total)", "total_ads");
        new Chart($("#ads-per-party"), totalAdsDoughnutChartConfig);

        // Add spending line chart
        let spendingLineChartConfig = generateLineGraphConfig(adData, "Average (Estimated) Spending over Time per Party", "spending_data");
        spendingLineChartConfig.options.scales.yAxes = [{
            ticks: {
                callback: function (value, index, values) {
                    return "€" + value.toFixed(2).toString();
                }
            }
        }];

        spendingLineChartConfig.options.tooltips = {
            intersect: false,
            callbacks: {
                label: function (tooltipItems, data) {
                    return "€" + tooltipItems.yLabel.toFixed(2).toString();
                }
            }
        };
        new Chart($("#spending-over-time-chart"), spendingLineChartConfig);

        // Add total ads doughnut chart
        let spendingDoughnutChartConfig = generateDoughnutChart(adData, "Total (Estimated) Spending per Party", "total_spending");
        spendingDoughnutChartConfig.options.tooltips.callbacks.label = function (tooltipItem, data){
            return "€" + addPercentageToDoughnutLabel(tooltipItem, data);
        };

        new Chart($("#spending-per-party"), spendingDoughnutChartConfig);
        $("#spending-total").text("€" + adData["total_spending"].toFixed(2).toString());

        // Add impressions line chart
        let impressionsLineChartConfig = generateLineGraphConfig(adData, "Average Estimated Impressions per Day", "impressions_data");
        new Chart($("#impressions-over-time-chart"), impressionsLineChartConfig);

        // Add impressions doughnut chart
        let impressionsDoughnutChartConfig = generateDoughnutChart(adData, "Total (Estimated) Impressions per Party", "total_impressions");
        new Chart($("#impressions-per-party"), impressionsDoughnutChartConfig);

        // Add potential reach line chart
        let potentialReachLineChartConfig = generateLineGraphConfig(adData, "Average Potential Reach per Day", "potential_reach");
        new Chart($("#potential-reach-chart"), potentialReachLineChartConfig);
        $("#missing-potential-reach").text(adData["missing_potential_reach"]);
        $("#total-ads").text(adData["total_ads"]);
    });
});
