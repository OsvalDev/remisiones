const getImportes = async () => {    
    let url;
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/getImportes';
    } else {        
        url = '/registro/getImportes';
    }    

    try {
        const response = await fetch(url, {            
            headers: {
                'Content-Type': 'application/json'
            },            
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const responseData = await response.json();
        
        if (responseData.result === 'failed') {
            throw new Error(`Error en la solicitud: ${responseData.data}`);
        }else{
            return responseData.data
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

const getTotalCostumers = async () => {    
    let url;
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/getTotalCostumers';
    } else {        
        url = '/registro/getTotalCostumers';
    }    

    try {
        const response = await fetch(url, {            
            headers: {
                'Content-Type': 'application/json'
            },            
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const responseData = await response.json();
        
        if (responseData.result === 'failed') {
            throw new Error(`Error en la solicitud: ${responseData.data}`);
        }else{
            return responseData.data
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};


window.addEventListener("load", async function() {    
    const data = await getTotalCostumers();
    const getChartOptions = () => {
        return {
            series: data[1],
            colors: ["#1C64F2", "#16BDCA", "#FDBA8C", "#E74694", "#7F3992", "#008080", "#FF6347", "#4CAF50", "#FFD700", "#FF69B4"],
            chart: {                                
            width: "100%",
            type: "donut",
            },
            stroke: {
            colors: ["transparent"],
            lineCap: "",
            },
            plotOptions: {
            pie: {
                donut: {
                labels: {
                    show: true,
                    name: {
                    show: true,
                    fontFamily: "Inter, sans-serif",
                    offsetY: 20,
                    },
                    total: {
                    showAlways: true,
                    show: true,
                    label: "Total",
                    fontFamily: "Inter, sans-serif",
                    formatter: function (w) {
                        const sum = w.globals.seriesTotals.reduce((a, b) => {
                        return a + b
                        }, 0)
                        return `$ ${sum.toLocaleString()}`
                    },
                    },
                    value: {
                    show: true,
                    fontFamily: "Inter, sans-serif",
                    offsetY: -20,
                    formatter: function (value) {
                        return value + "k"
                    },
                    },
                },
                size: "80%", }, }, },
            grid: {
            padding: { top: -2, }, },
            labels: data[0],
            dataLabels: { enabled: false, },
            legend: { show: false ,position: "top",
            fontFamily: "Inter, sans-serif", },
            yaxis: {
            labels: {
                formatter: function (value) { return "$" + value.toLocaleString() }, }, },
            xaxis: {
            labels: { formatter: function (value) { return "$" + value.toLocaleString()  }, },
            axisTicks: { show: false, },
            axisBorder: { show: false, }, },
        }
    }

    if (document.getElementById("donut-chart") && typeof ApexCharts !== 'undefined') {
    const chart = new ApexCharts(document.getElementById("donut-chart"), getChartOptions());
    chart.render();

    }
});

window.addEventListener("load", async function() {
    const importes = await getImportes();
const options = {                                
        series: [
        {
            name: "Monto",
            color: "#db2777",
            data: [
            { x: "Remisionado", y: parseFloat(importes[0].toFixed(2)) },                                    
            { x: "Facturado", y: parseFloat(importes[1].toFixed(2)) }
            ],
        }
        ],
        chart: {
        type: "bar",                                
        toolbar: { show: false, }, },
        plotOptions: {
        bar: { horizontal: false, columnWidth: "70%",
            borderRadiusApplication: "end", borderRadius: 8, }, },
        tooltip: { shared: true, intersect: false,
        style: { fontFamily: "Inter, sans-serif", }, },
        states: { hover: { filter: { type: "darken", value: 1, }, }, },
        stroke: { show: true, width: 0, colors: ["transparent"], },
        grid: { show: false, strokeDashArray: 4,
            padding: {left: 2, right: 2, top: -14 },
        },
        dataLabels: { enabled: true, formatter: function (value) { return "$ " + value.toLocaleString()  }, },
        legend: { show: false, },
        xaxis: {
        floating: false,
        labels: {            
            show: true,
            style: { fontFamily: "Inter, sans-serif",
            cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
            }
        },
        axisBorder: { show: false, }, axisTicks: { show: false, },
        },
        yaxis: { show: true, },
        fill: { opacity: 1, },
    }

    if(document.getElementById("column-chart") && typeof ApexCharts !== 'undefined') {
        const chart = new ApexCharts(document.getElementById("column-chart"), options);
        chart.render();
    }
});