$(document).ready(function () {
    $.getJSON("data/data.json", function (adData) {
        $("#last-updated").text(adData["last_updated"]);

        // Add active ads line chart
        let activeAdsLineChartConfig = generateLineGraphConfig(adData, "Ads Active over time", "active-ads-per-date");
        new Chart($("#active-ads-over-time"), activeAdsLineChartConfig);
        $(".total-ads").text(adData["ads-total"]);

        // Add total ads bar chart
        let totalAdsBarChartConfig = generateBarChart(adData, "Total Ads", "ads-per-party");
        new Chart($("#ads-per-party"), totalAdsBarChartConfig);

        // Add spending line chart
        let spendingLineChartConfig = generateLineGraphConfig(adData, "Average (Estimated) Spending over time", "spending-per-date");
        new Chart($("#spending-over-time-chart"), spendingLineChartConfig);

        // Add total ads bar chart
        let spendingBarChartConfig = generateBarChart(adData, "Total (Estimated) Spending", "spending-per-party");
        new Chart($("#spending-per-party"), spendingBarChartConfig);

        $("#spending-total-lower").text("€" + adData["spending-range"]["lower"]);
        $("#spending-total-upper").text("€" + adData["spending-range"]["upper"]);
        $("#most-expensive-ad-cost").text("€" + adData["most-expensive-ad"]["cost"].toFixed(2));
        $("#most-expensive-ad-party").text(adData["most-expensive-ad"]["party"]);
        $("#most-expensive-ad-days").text(adData["most-expensive-ad"]["days"]);
        $("#most-expensive-ad-link").attr("href", $("#most-expensive-ad-link").attr("href") + adData["most-expensive-ad"]["id"]);

        // Add impressions line chart
        let impressionsLineChartConfig = generateLineGraphConfig(adData, "Average (Estimated) Impressions over time", "impressions-per-date");
        new Chart($("#impressions-over-time-chart"), impressionsLineChartConfig);

        // Add impressions bar chart
        let impressionsBarChartConfig = generateBarChart(adData, "Total (Estimated) Impressions", "impressions-per-party");
        new Chart($("#impressions-per-party"), impressionsBarChartConfig);

        // Add potential reach line chart
        let potentialReachLineChartConfig = generateLineGraphConfig(adData, "Average Potential Reach over time", "potential-reach-per-date");
        potentialReachLineChartConfig.options.scales.xAxes[0].ticks = {min: new Date("2020-03-31")};
        new Chart($("#potential-reach-chart"), potentialReachLineChartConfig);
        $("#missing-potential-reach").text(adData["ads-without-potential-reach"]);
    });
});
