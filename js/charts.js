$(document).ready(function () {
    $.getJSON("data.json", function (party_ad_data) {
        $('#last-updated').text(party_ad_data.last_updated);

        // Add active ads line chart
        let activeAdsLineChartConfig = generateLineGraphConfig(party_ad_data, "Ads Active per Day", "active_ads");
        new Chart($("#active_ads_per_day_chart"), activeAdsLineChartConfig);

        // Add total ads doughnut chart
        let totalAdsDoughnutChartConfig = generateDoughnutChart(party_ad_data, "Total Ads per Party (" + party_ad_data.total_ads + " total)", "total_ads");
        new Chart($("#total_active_ads_chart"), totalAdsDoughnutChartConfig);

        // Add spending line chart
        let spendingLineChartConfig = generateLineGraphConfig(party_ad_data, "Average (Estimated) Spending over Time per Party", "spending_data");
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
        new Chart($("#spend_per_day_chart"), spendingLineChartConfig);

        // Add total ads doughnut chart
        let spendingDoughnutChartConfig = generateDoughnutChart(party_ad_data, "Total (Estimated) Spending per Party", "total_spending");
        spendingDoughnutChartConfig.options.tooltips.callbacks.label = function (tooltipItem, data){
            return "€" + addPercentageToDoughnutLabel(tooltipItem, data);
        };

        new Chart($("#total_spend_chart"), spendingDoughnutChartConfig);
        $('#total-spending').text("€" + party_ad_data.total_spending.toFixed(2).toString());

        // Add impressions line chart
        let impressionsLineChartConfig = generateLineGraphConfig(party_ad_data, "Average Estimated Impressions per Day", "impressions_data");
        new Chart($("#impressions_per_day_chart"), impressionsLineChartConfig);

        // Add impressions doughnut chart
        let impressionsDoughnutChartConfig = generateDoughnutChart(party_ad_data, "Total (Estimated) Impressions per Party", "total_impressions");
        new Chart($("#total_impressions_chart"), impressionsDoughnutChartConfig);

        // Add potential reach line chart
        let potentialReachLineChartConfig = generateLineGraphConfig(party_ad_data, "Average Potential Reach per Day", "potential_reach");
        new Chart($("#potential_reach_per_day_chart"), potentialReachLineChartConfig);
        $('#missing-potential-reach').text(party_ad_data.missing_potential_reach);
        $('#total-ads').text(party_ad_data.total_ads);
    });
});
