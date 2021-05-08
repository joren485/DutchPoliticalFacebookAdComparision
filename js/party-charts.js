$(document).ready(function () {

    let searchParams = new URLSearchParams(window.location.search)

    if (!searchParams.has("party")) {
        $("#party-specific-charts").append("<p>No Party Provided.</p>");
        return;
    }

    let party = searchParams.get("party");

    if (!PARTIES.includes(party)) {
        $("#party-specific-charts").append("<p>Party Not Found.</p>");
        return;
    }

    $.getJSON("data/parsed_data/" + party + ".json", function (partyAdData) {
        $("#last-updated").text(partyAdData["last-updated"]);

        $("#party-specific-charts").append(
            `<div class="text-center">
                <h1>${party} Graphs</h1>
                <p class="lead">${party} ran <strong>${partyAdData['total-ads']}</strong> ads and spent between <strong>€${partyAdData['spending-total-range'][0]}</strong> and <strong>€${partyAdData['spending-total-range'][1]}</strong>.</p>
            </div>
            <hr>`);

        ["Spending", "Impressions"].forEach(function (dataType) {

            let dataTypeLowerCase = dataType.toLowerCase();
            let datatypeDivId = party + "-" + dataTypeLowerCase
            let datatypeDivChartsId = party + "-" + dataTypeLowerCase + "-charts"

            $("#party-specific-charts").append(
                `<div id="${datatypeDivId}">
                    <div class="text-center">
                        <h2>${dataType}</h2>
                    </div>
                    <div id="${datatypeDivChartsId}">
                    </div>
                 </div>`
            );

            ["Region", "Gender", "Age"].forEach(function (labelType) {

                let labelTypeLowerCase = labelType.toLowerCase();

                let LineChartCanvasId = party.toLowerCase() + "-" + labelTypeLowerCase + "-" + dataTypeLowerCase + "-line-chart";
                let BarChartCanvasId = party.toLowerCase() + "-" + labelTypeLowerCase + "-" + dataTypeLowerCase + "-bar-chart";

                $("#" + datatypeDivChartsId).append(
                    `<div>
                    <div class="text-center">
                        <h4>(Estimated) ${dataType} per ${labelType} (${party})</h4>
                    </div>
                    
                    <div class="row">
                        <div class="col-8">
                            <canvas id="${LineChartCanvasId}"></canvas>
                            <p>This graph shows ${dataTypeLowerCase} per ${labelTypeLowerCase} over time. Facebook provides a range (e.g. €1000 - €1999 has been spent on an ad) for each ad, this graph is based on the average of the range of each ad.</p>
                        </div>
                        <div class="col-4">
                            <canvas id="${BarChartCanvasId}"></canvas>
                        </div>
                    </div>
                </div>
                <hr>`);

                let labels;
                if (labelType === "Region") {
                    labels = REGIONS;
                } else if (labelType === "Gender"){
                    labels = GENDERS;
                }else if (labelType === "Age"){
                    labels = AGE_RANGES;
                }

                let lineChart = generateLineGraphConfig(
                    "Average (Estimated) " + dataType + " per " + labelType + " over time (" + party + ")",
                    partyAdData,
                    dataTypeLowerCase + "-per-" + labelTypeLowerCase + "-per-date",
                    labels);
                new Chart($("#" + LineChartCanvasId), lineChart);

                let barChart = generateBarChart(
                    "Total (Estimated) " + dataType + " per " + labelType + " (" + party + ")",
                    partyAdData,
                    dataTypeLowerCase + "-per-" + labelTypeLowerCase,
                    labels);
                new Chart($("#" + BarChartCanvasId), barChart);
            })
        });
    });
});
