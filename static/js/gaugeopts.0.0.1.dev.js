//refresh dev file

//SHT Project
//Gauge Options
//Marcus Dechant (c)
//v0.0.1

var optsTemp = {
    angle: -0, 
    lineWidth: 0.4, 
    radiusScale: 0.95, 
    pointer: {
        length: 0.6, 
        strokeWidth: 0.035, 
        color: '#6D6D6D' 
    },
    limitMax: false,     
    limitMin: false,     
    staticZones: [
        {strokeStyle: "red", min: 0, max: 12.4},
        {strokeStyle: "orange", min: 12.5, max: 18.9},
        {strokeStyle: "green", min: 19, max: 25.9 },
        {strokeStyle: "orange", min: 26, max: 32.5},
        {strokeStyle: "red", min: 32.6, max: 45},
    ],
    strokeColor: '#E0E0E0',
    highDpiSupport: true, 
    staticLabels: {
        font: "10px sans-serif",
        labels: [0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
        color: "#6D6D6D",
    },
};
var optsHumi = {
    angle: -0, 
    lineWidth: 0.4, 
    radiusScale: 0.95, 
    pointer: {
        length: 0.6, 
        strokeWidth: 0.035,
        color: '#6D6D6D'
    },
    limitMax: false,
    limitMin: false,
    staticZones: [
        {strokeStyle: "red", min: 0, max: 10.9},
        {strokeStyle: "orange", min:11 , max: 20.9},
        {strokeStyle: "green", min: 21, max: 50.9},
        {strokeStyle: "orange", min: 51, max: 85.9},
        {strokeStyle: "red", min: 85, max: 100},
    ],
    strokeColor: '#E0E0E0',
    highDpiSupport: true,
    staticLabels: {
        font: "10px sans-serif",
        labels: [0, 10, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
        color: "#6D6D6D",
    },
};