const COLORS = {
    'VVD': '#ff7709',
    'FvD': '#841818',
    'GL': '#50c401',
    'DENK': '#41bac2',
    'D66': '#01af40',
    'CDA': '#007b5f',
    '50P': '#92278f',
    'PvdA': '#0060aa',
    'SGP': '#024a90',
    'CU': '#012466',
    'SP': '#fe0000',
    'PvdD': '#006c2e',

    'male': '#0000ff',
    'female': '#ffc0cb',

    '13-17': '#641E16',
    '18-24': '#512E5F',
    '25-34': '#154360',
    '35-44': '#0E6251',
    '45-54': '#145A32',
    '55-64': '#7D6608',
    '65+': '#784212',

    'male-13-17': '#641E16',
    'female-13-17': '#512E5F',
    'male-18-24': '#0E6251',
    'female-18-24': '#145A32',
    'male-25-34': '#784212',
    'female-25-34': '#943126',
    'male-35-44': '#21618C',
    'female-35-44': '#0E6655',
    'male-45-54': '#9C640C',
    'female-45-54': '#873600',
    'male-55-64': '#515A5A',
    'female-55-64': '#2C3E50',
    'male-65+': '#2471A3',
    'female-65+': '#FAD7A0',

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
            responsive: true,
            title: {
                display: true,
                text: title,
                fontSize: 18,
            },
            legend: {
                position: "bottom",
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
            maintainAspectRatio: false,
            responsive: true,
            title: {
                display: true,
                text: title,
                fontSize: 18,
            },
            legend: {
                position: "bottom",
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

        for (let party in adData["party-specific-data"]) {
            chartConfig.data.labels.push(party);
            chartConfig.data.datasets[0].data.push(adData["party-specific-data"][party][dataKey])
            chartConfig.data.datasets[0].backgroundColor.push(COLORS[party])
        }
    }

    return chartConfig;
}