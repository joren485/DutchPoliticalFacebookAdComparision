$(document).ready(function () {

    PARTIES.forEach(function (party) {
        $("#party-specific-text-charts-navbar-dropdown").append(`<a class="dropdown-item" href="party-text.html?party=${party}">${party}</a>`);
    });

    let searchParams = new URLSearchParams(window.location.search)

    if (!searchParams.has("party")) {
        $("#party-specific-text-charts").append("<p>No Party Provided.</p>");
        return;
    }

    let party = searchParams.get("party");

    if (!PARTIES.includes(party)) {
        $("#party-specific-text-charts").append("<p>Party Not Found.</p>");
        return;
    }

    $.getJSON("data/parsed_data/text-" + party + ".json", function (partyAdTextData) {
        $("#last-updated").text(partyAdTextData["last-updated"]);

        $("#party-specific-text-charts").append(
            `<div class="text-center">
                <h1>${party} Text Analysis Graphs</h1>
            </div>
            <hr>`);
        DEMOGRAPHICS.forEach(function (demographic){

            let demographicSlug = demographic.replace("+", "").toLowerCase()
            let demographicChartsDivId = party + "-" + demographicSlug + "-charts";


            $("#party-specific-text-charts").append(
                `<div">
                    <div class="text-center">
                        <h2>${demographic}</h2>
                    </div>
                    <div id="${demographicChartsDivId}"></div>
                 </div>`
            );

            ["Occurrences", "Impressions", "Potential Reach"].forEach(function (dataType) {
                let dataTypeSlug = dataType.replace(" ", "-").toLowerCase()
                let datatypeDivBarChartId = party + "-" + demographicSlug + "-" + dataTypeSlug + "-bar-chart"

                $("#" + demographicChartsDivId).append(
                    `<div class="col-6 mx-auto">
                        <canvas id="${datatypeDivBarChartId}"></canvas>
                     </div>
                     <hr>`
                );

                let key = dataTypeSlug + "-" + demographic.toLowerCase();

                let barChart = generateBarChart(
                    dataType,
                    partyAdTextData[key],
                    "data",
                    partyAdTextData[key]["labels"]);
                barChart.options.maintainAspectRatio = true;
                new Chart($("#" + datatypeDivBarChartId), barChart);
            });
        });
    });
});
