const COLORS = {

    '50P': '#92278f',
    'BIJ1': '#ee047e',
    'CDA': '#007b5f',
    'CU': '#012466',
    'CO': '#eb984e',
    'DENK': '#41bac2',
    'D66': '#01af40',
    'FvD': '#841818',
    'GL': '#50c401',
    'JA21': '#242B57',
    'PVV': '#212F3D',
    'PvdA': '#C0392B',
    'PvdD': '#006c2e',
    'SGP': '#024a90',
    'SP': '#fe0000',
    'VOLT': '#512e5f',
    'VVD': '#ff7709',

    'Male': '#0000ff',
    'Female': '#ffc0cb',

    '13-17': '#641E16',
    '18-24': '#512E5F',
    '25-34': '#154360',
    '35-44': '#0E6251',
    '45-54': '#145A32',
    '55-64': '#7D6608',
    '65+': '#784212',

    'Drenthe': '#AED6F1',
    'Friesland': '#AF7AC5',
    'Gelderland': '#E74C3C',
    'Groningen': '#ABEBC6',
    'Limburg': '#1A5276',
    'Noord-Brabant': '#F2D7D5',
    'Noord-Holland': '#239B56',
    'Utrecht': '#F4D03F',
    'Zeeland': '#D7BDE2',
    'Zuid-Holland': '#EB984E',
    'Overijssel': '#B7950B',
    'Flevoland': '#E59866',
};

const PARTIES = ["50P", "BIJ1", "CDA", "CU", "CO", "D66", "DENK", "FvD", "GL", "JA21", "PVV", "PvdA", "PvdD", "SGP", "SP", "VOLT", "VVD"];

function percentageBarGraph(tooltipItems, data) {
    let dataset = data.datasets[tooltipItems.datasetIndex];
    let value = dataset.data[tooltipItems.index];

    let total = 0;
    dataset.data.forEach(function (element) {
        total += element;
    });

    if (total === 0) {
        return 0;
    }

    return (value / total * 100).toFixed(2);
}

function percentageLineGraph(tooltipItems, data) {

    let total = 0;
    data.datasets.forEach(function (dataset) {
        total += dataset.data[tooltipItems.index]
    });

    if (total === 0){
        return 0;
    }
    return (tooltipItems.yLabel / total * 100).toFixed(2);
}

function getDaysArray(startDate) {
    let dates = [];
    let now = new Date();
    for (let dt = new Date(startDate); dt <= now; dt.setDate(dt.getDate() + 1)) {
        dates.push(new Date(dt).toISOString().split('T')[0]);
    }
    return dates;
}

function generateLineGraphConfig(adData, title, dataKey, specificParty = "") {

    let scales = {
        xAxes: [{
            ticks: {},
            type: "time",
            time: {
                unit: "day",
                stepSize: 1,
            }
        }],
        yAxes: [{
            ticks: {},
        }]
    };

    let tooltips = {
        mode: 'index',
        intersect: false,
        position: "nearest",
        callbacks: {
            label: function (tooltipItems, data) {
                let percentage = percentageLineGraph(tooltipItems, data);
                return data.datasets[tooltipItems.datasetIndex].label + ": " + tooltipItems.yLabel.toFixed(2) + " (" + percentage + "%)";
            },
        },
    };
    if (dataKey.toLowerCase().includes("spending")) {

        scales.yAxes[0].ticks.callback = function (value, index, values) {
                return "€" + value.toFixed(2).toString();
        };
        tooltips.callbacks.label = function (tooltipItems, data) {
            let percentage = percentageLineGraph(tooltipItems, data);
            return data.datasets[tooltipItems.datasetIndex].label + ": €" + tooltipItems.yLabel.toFixed(2) + " (" + percentage + "%)";
        }
    }

    if (specificParty) {
        scales.yAxes[0].stacked = true;
    }

    let graphConfig = {
        type: "line",
        data: {
            labels: getDaysArray(new Date(adData["start-date"])),
            datasets: []
        },
        options: {
            animation: {
                duration: 0
            },
            hover: {
                animationDuration: 0
            },
            responsiveAnimationDuration: 0,
            responsive: true,
            title: {
                display: true,
                text: title,
                fontSize: 16,
            },
            legend: {
                position: "bottom",
                labels: {padding: 7,},
            },
            scales: scales,
            tooltips: tooltips,
            plugins: {
                zoom: {
                    zoom: {
                        enabled: true,
                        drag: true,
                        mode: "x",
                    }
                }
            },
        },
    };

    if (specificParty) {
        for (let key in adData["party-specific-data"][specificParty][dataKey]) {
            graphConfig.data.datasets.push(
                {
                    label: key,
                    data: adData["party-specific-data"][specificParty][dataKey][key],
                    fill: true,
                    backgroundColor: COLORS[key],
                    borderColor: COLORS[key],
                    pointRadius: 0,
                    borderWidth: 2,
                });
        }


    } else {
        for (let party in adData["party-specific-data"]) {
            graphConfig.data.datasets.push(
                {
                    label: party,
                    data: adData["party-specific-data"][party][dataKey],
                    fill: false,
                    backgroundColor: COLORS[party],
                    borderColor: COLORS[party],
                    pointRadius: 0,
                    borderWidth: 2,
                });
        }
    }

    return graphConfig;
}

function generateBarChart(adData, title, dataKey, specificParty = "") {

    let scales = {
        xAxes: [
            {
                ticks: {
                    beginAtZero: true,
                },
            }],
        yAxes: [{}],
    }

    let tooltips = {
        intersect: false,
        callbacks: {
            label: function (tooltipItems, data) {

                let dataset = data.datasets[tooltipItems.datasetIndex];
                let value = dataset.data[tooltipItems.index];

                let percentage = percentageBarGraph(tooltipItems, data);
                return value.toFixed(2) + " (" + percentage + "%)";
            },
        },
    };

    if (dataKey.toLowerCase().includes("spending")) {
        scales.xAxes[0].ticks.callback = function (value, index, values) {
                return "€" + value.toFixed(2).toString();
        };

        tooltips.callbacks.label = function (tooltipItems, data) {

            let dataset = data.datasets[tooltipItems.datasetIndex];
            let value = dataset.data[tooltipItems.index];

            let percentage = percentageBarGraph(tooltipItems, data);
            return "€" + value.toFixed(2) + " (" + percentage + "%)";
        };
    }
    let chartConfig = {
        type: "horizontalBar",
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [],
                maxBarThickness: 30,
            }]
        },
        options: {
            animation: {
                duration: 0
            },
            hover: {
                animationDuration: 0
            },
            responsiveAnimationDuration: 0,
            maintainAspectRatio: false,
            responsive: true,
            title: {
                display: true,
                text: title,
                fontSize: 16,
            },
            legend: {
                display: false,
            },
            tooltips: tooltips,
            scales: scales,
        }
    };

    if (specificParty) {

        adData["party-specific-data"][specificParty][dataKey]['order'].forEach(function (key) {
            chartConfig.data.labels.push(key);
            chartConfig.data.datasets[0].data.push(adData["party-specific-data"][specificParty][dataKey]['map'][key])
            chartConfig.data.datasets[0].backgroundColor.push(COLORS[key])
        });


    } else {
        adData[dataKey]['order'].forEach(function (party) {
            chartConfig.data.labels.push(party);
            chartConfig.data.datasets[0].data.push(adData[dataKey]['map'][party])
            chartConfig.data.datasets[0].backgroundColor.push(COLORS[party])
        });
    }

    return chartConfig;
}

$(document).ready(function () {
    PARTIES.forEach(function (party) {
        $("#party-specific-charts-navbar-dropdown").append(`<a class="dropdown-item" href="party.html?party=${party}">${party}</a>`);
    });
});