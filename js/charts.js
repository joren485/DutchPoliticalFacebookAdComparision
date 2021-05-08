$(document).ready(function () {
    $.getJSON("data/parsed_data/general-data.json", function (generalAdData) {
        $("#last-updated").text(generalAdData["last-updated"]);

        // Add active ads line chart
        let activeAdsLineChartConfig = generateLineGraphConfig("Ads Active over Time", generalAdData, "active-ads-per-party-per-date");
        new Chart($("#active-ads-over-time"), activeAdsLineChartConfig);
        $(".total-ads").text(generalAdData["ads-total"]);

        // Add total ads bar chart
        let totalAdsBarChartConfig = generateBarChart("Total Ads", generalAdData,"ads-per-party");
        new Chart($("#ads-per-party"), totalAdsBarChartConfig);

        // Add spending line chart
        let spendingLineChartConfig = generateLineGraphConfig("Average (Estimated) Spending over Time", generalAdData, "spending-per-party-per-date");
        new Chart($("#spending-over-time-chart"), spendingLineChartConfig);

        // Add total ads bar chart
        let spendingBarChartConfig = generateBarChart("Total (Estimated) Spending", generalAdData, "spending-per-party");
        new Chart($("#spending-per-party"), spendingBarChartConfig);

        $("#spending-total-lower").text("€" + generalAdData["spending-total-range"][0]);
        $("#spending-total-upper").text("€" + generalAdData["spending-total-range"][1]);
        $("#most-expensive-ad-cost").text("€" + generalAdData["most-expensive-ad"]["cost"]);
        $("#most-expensive-ad-party").text(generalAdData["most-expensive-ad"]["party"]);
        $("#most-expensive-ad-days").text(generalAdData["most-expensive-ad"]["days"]);
        $("#most-expensive-ad-link").attr("href", $("#most-expensive-ad-link").attr("href") + generalAdData["most-expensive-ad"]["id"]);

        // Add impressions line chart
        let impressionsLineChartConfig = generateLineGraphConfig("Average (Estimated) Impressions over Time", generalAdData,"impressions-per-party-per-date");
        new Chart($("#impressions-over-time-chart"), impressionsLineChartConfig);

        // Add impressions bar chart
        let impressionsBarChartConfig = generateBarChart("Total (Estimated) Impressions", generalAdData, "impressions-per-party");
        new Chart($("#impressions-per-party"), impressionsBarChartConfig);

        // Add potential reach line chart
        let potentialReachLineChartConfig = generateLineGraphConfig("Average Potential Reach over Time", generalAdData,"potential-reach-per-party-per-date");
        potentialReachLineChartConfig.options.scales.xAxes[0].ticks.min = new Date("2020-03-31");
        new Chart($("#potential-reach-chart"), potentialReachLineChartConfig);
        $("#missing-potential-reach").text(generalAdData["ads-without-potential-reach"]);
    });
});
