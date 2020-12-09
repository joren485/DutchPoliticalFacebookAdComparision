const COLORS = {
    'VVD': '#ff7709',
    'FvD': '#841818',
    'GL': '#50c401',
    'DENK': '#41bac2',
    'D66': '#01af40',
    'CDA': '#007b5f',
    '50P': '#92278f',
    'PvdA': '#C0392B',
    'SGP': '#024a90',
    'CU': '#012466',
    'SP': '#fe0000',
    'PvdD': '#006c2e',
    'PVV': '#212F3D',

    'male': '#0000ff',
    'female': '#ffc0cb',

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
    'Limburg': '#E74C3C',
    'North Brabant': '#E74C3C',
    'Noord-Holland': '#239B56',
    'Utrecht': '#F4D03F',
    'Zeeland': '#D7BDE2',
    'Zuid-Holland': '#EB984E',
    'Overijssel': '#B7950B',
    'Flevoland': '#EB984E',
}


function addPercentageToDoughnutLabel(tooltipItem, data) {
    // https://stackoverflow.com/questions/37257034/chart-js-2-0-doughnut-tooltip-percentages/49717859#49717859
    let dataset = data.datasets[tooltipItem.datasetIndex];
    let total = dataset._meta[Object.keys(dataset._meta)[0]].total;
    let value = dataset.data[tooltipItem.index];
    let percentage = (value / total * 100).toFixed(2);
    return value.toFixed(2) + " (" + percentage + "%)";
}

function getDaysArray(startDate) {
    let dates = [];
    let now = new Date();
    for (let dt = new Date(startDate); dt <= now; dt.setDate(dt.getDate() + 1)) {
        dates.push(new Date(dt).toISOString().split('T')[0]);
    }
    return dates;
}

function addPartiesNavBar(parties) {
    for (let party in parties) {
        $("#party-specific-charts-navbar-dropdown").append(`<a class="dropdown-item" href="party.html?party=${party}">${party}</a>`);
    }
}

function generateLineGraphConfig(adData, title, dataKey, specificParty = "") {
    let graphConfig = {
        type: "line",
        data: {
            labels: getDaysArray(new Date("2020-01-01")),
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
                fontSize: 18,
            },
            legend: {
                position: "bottom",
                                labels: {padding: 7,},
            },
            scales: {
                xAxes: [{
                    type: "time",
                }],
            },
            tooltips: {
                mode: 'x',
                intersect: false,
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                    },
                    zoom: {
                        enabled: true,
                        drag: false,
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
                    fill: false,
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

function generateDoughnutChart(adData, title, dataKey, specificParty = "") {
    let chartConfig = {
        type: "doughnut",
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [],
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
                fontSize: 18,
            },
            legend: {
                position: "bottom",
                labels: {
                    padding: 5,
                },
            },
            tooltips: {
                callbacks: {
                    label: addPercentageToDoughnutLabel,
                    title: function (tooltipItem, data) {
                        return data.labels[tooltipItem[0].index];
                    }
                }
            },
        }
    };

    if (specificParty) {
        for (let key in adData["party-specific-data"][specificParty][dataKey]) {
            chartConfig.data.labels.push(key);
            chartConfig.data.datasets[0].data.push(adData["party-specific-data"][specificParty][dataKey][key])
            chartConfig.data.datasets[0].backgroundColor.push(COLORS[key])
        }

    } else {

        for (let party in adData[dataKey]) {
            chartConfig.data.labels.push(party);
            chartConfig.data.datasets[0].data.push(adData[dataKey][party])
            chartConfig.data.datasets[0].backgroundColor.push(COLORS[party])
        }
    }

    return chartConfig;
}

$(document).ready(function () {
    $.getJSON("data.json", function (adData) {
        $("#last-updated").text(adData["last_updated"]);
        addPartiesNavBar(adData["party-specific-data"]);
    });
});