$(document).ready(function () {
    $.getJSON("data.json", function (adData) {
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

        let regionChartCanvasId = party.toLowerCase() + "-region-chart";
        let genderChartCanvasId = party.toLowerCase() + "-gender-chart";
        let ageChartCanvasId = party.toLowerCase() + "-age-chart";
        let genderAgeChartCanvasId = party.toLowerCase() + "-gender-age-chart";

        let partyChartsHTML = `<div id="${party.toLowerCase()}-charts">
            <div class="text-center">
                <h2>${party} Charts</h2>
            </div>
            <div>
                 <div>
                    <div class="text-center">
                        <h3>Impressions per Region (${party})</h3>
                    </div>
                    <canvas id="${regionChartCanvasId}"></canvas>
                </div>

                <hr>
                <div>
                    <div class="text-center">
                        <h3>Impressions per Gender (${party})</h3>
                    </div>
                    <canvas id="${genderChartCanvasId}"></canvas>
                </div>

                <hr>

                <div>
                    <div class="text-center">
                        <h3>Impressions per Age (${party})</h3>
                    </div>
                    <canvas id="${ageChartCanvasId}"></canvas>
                </div>

                <hr>

                <div>
                    <div class="text-center">
                        <h3>Impressions per Gender and Age (${party})</h3>
                    </div>
                    <canvas id="${genderAgeChartCanvasId}"></canvas>
                </div>
            </div>
            <hr>
        </div>`;

        $('#party-specific-charts').append(partyChartsHTML);

        let partyRegionLineChart = generateLineGraphConfig(adData,
            "Impressions per Region per Day (" + party + ")",
            "impressions-per-region-per-date",
            party);
        new Chart($("#" + regionChartCanvasId), partyRegionLineChart);

        let partyGenderLineChart = generateLineGraphConfig(adData,
            "Impressions per Gender per Day (" + party + ")",
            "impressions-per-gender-per-date",
            party);
        new Chart($("#" + genderChartCanvasId), partyGenderLineChart);

        let partyAgeLineChart = generateLineGraphConfig(adData,
            "Impressions per Age per Day (" + party + ")",
            "impressions-per-age-per-date",
            party);
        new Chart($("#" + ageChartCanvasId), partyAgeLineChart);

        let partyGenderAgeLineChart = generateLineGraphConfig(adData,
            "Impressions per Gender and Age per Day (" + party + ")",
            "impressions-per-gender-and-age-per-date",
            party);
        new Chart($("#" + genderAgeChartCanvasId), partyGenderAgeLineChart);
    });
});
