Plotly.d3.csv('prison_list.csv', function(err, rows){

function unpack(rows, key) {
    return rows.map(function(row) { return row[key]; });
}

var state = unpack(rows, 'State'),
    prison = unpack(rows, 'Prison'),
    prisonCap = unpack(rows, 'Capacity'),
    prisonStatus = unpack(rows, 'Status'),
    prisonLat = unpack(rows, 'Latitude'),
    prisonLon = unpack(rows, 'Longitudue'),
    color = [,"rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"],
    prisonSize = [],
    hoverText = [],
    scale = 50000;

for ( var i = 0 ; i < prisonCap.length; i++) {
    var currentSize = prisonCap[i] / scale;
    var currentText = prison[i] + " pop: " + prisonCap[i];
    prisonSize.push(currentSize);
    hoverText.push(currentText);
}

var data = [{
    type: 'scattergeo',
    locationmode: 'AUS',
    lat: prisonLat,
    lon: prisonLon,
    hoverinfo: 'text',
    text: hoverText,
    marker: {
        size: prisonSize,
        line: {
            color: 'black',
            width: 2
        },
    }
}];

var layout = {
    title: 'Australian Prisons',
    showlegend: false,
    geo: {
        scope: 'world',
        center: {
            lon: 130.5,
            lat: -22.5
        },
        projection: {
            type: 'mercator'
        },
        showland: true,
        landcolor: 'rgb(217, 217, 217)',
        subunitwidth: 1,
        countrywidth: 1,
        subunitcolor: 'rgb(255,255,255)',
        countrycolor: 'rgb(255,255,255)'
    },
};

Plotly.newPlot("myDiv", data, layout, {showLink: false});

});