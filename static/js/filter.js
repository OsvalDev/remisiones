const formatDate = (fechaString) => {
    const fecha = new Date(fechaString);
    const fechaFormateada = fecha.toISOString().split('T')[0];
    return fechaFormateada
}

const filterCostumerData = async () => {
    let url;
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/getRemissionByFilter';
    } else {        
        url = '/registro/getRemissionByFilter';
    }
    
    //recollect data
    var checkboxes = document.querySelectorAll('input[type="checkbox"].btnCostumerFilter:checked');
    var valuesCostumers = Array.from(checkboxes).map(checkbox => checkbox.value);
    
    checkboxes = document.querySelectorAll('input[type="checkbox"].statusFilter:checked');
    var valuesStatus = Array.from(checkboxes).map(checkbox => checkbox.value);

    const data = { costumers : valuesCostumers,
                    status: valuesStatus,
                    dateStart : document.getElementById('dateStart').value,
                    dateEnd : document.getElementById('dateEnd').value,
                    numRemision : document.getElementById('numRemision').value,
                    numCompra : document.getElementById('numCompraFilter').value };
    
    try {
        const response = await fetch(url, {            
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const responseData = await response.json();
        
        if (responseData.result === 'failed') {
            throw new Error(`Error en la solicitud: ${responseData.data}`);
        }else{            
            const existingAlert = document.getElementById('tableRows');
            if (existingAlert && existingAlert.parentNode) {
                existingAlert.parentNode.removeChild(existingAlert);
            }
            
            const existingContainerCard = document.getElementById('containerCards');
            if (existingContainerCard && existingContainerCard.parentNode) {
                existingContainerCard.parentNode.removeChild(existingContainerCard);
            }

            const tableBody = document.createElement('tbody');            
            tableBody.id = 'tableRows';

            const cardsContainer = document.createElement('div');            
            cardsContainer.id = 'containerCards';
            
            let contentRows = '';
            let contentCards = ''
            for (let data of responseData.data){                
                contentRows += `
                    <tr class="bg-white border-b hover:bg-gray-100" >
                        <td scope="row" class="max-w-40 text-wrap whitespace-normal" style="overflow-wrap: break-word;">
                            <a class="block w-full h-full py-4 px-4 text-wrap" href="remission/${ data[0] }/${ data[1] }">
                                ${ data[1] }  <!-- Número de compra -->
                            </a>                                        
                        </td>
                        <td class="w-32">
                            <a class="block w-full h-full py-4 px-4" href="remission/${ data[0] }/${ data[1] }">
                                ${ data[0] }<!-- Número de remision -->
                            </a>                                        
                        </td>
                        <td class="w-40">
                            <a class="block w-full h-full py-4 px-4" href="remission/${ data[0] }/${ data[1] }">
                                ${ formatDate( data[2] ) }<!-- fecha de registro -->
                            </a>                                        
                        </td>
                        <td class="w-80">
                            <a class="block w-full h-full py-4 px-2" href="remission/${ data[0] }/${ data[1] }">
                                ${ data[3] }  <!-- cliente -->
                            </a>                                        
                        </td>
                        <td class="w-32">
                            <a class="block w-full h-full py-4 px-4" href="remission/${ data[0] }/${ data[1] }">
                                $ ${ data[5] }<!-- importeRemisionado -->
                            </a>                                                                    
                        </td>
                        <td class="w-32">
                            <a class="block w-full h-full py-4 px-4" href="remission/${ data[0] }/${ data[1] }">
                                $ ${ data[6] }<!-- importeFacturado -->
                            </a>                                        
                        </td>                                
                        <td class="w-40">
                            <a class="block w-full h-full py-4 px-4" href="remission/${ data[0] }/${ data[1] }">
                                ${ data[4] }  <!-- estatus -->
                            </a>
                        </td>                                
                    </tr>
                `;

                contentCards += `
                <a href="remission/${ data[0] }/${ data[1] }" class="w-full h-fit">
                    <div class="shadow-lg w-full h-fit rounded-lg my-4 p-4 hover:bg-gray-200 flex flex-col items-center">
                        <div>
                            <p class="font-bold">
                                ${ data[3] }  <!-- cliente -->
                            </p>
                            <p>
                            #Remision: ${ data[1] }  <!-- Número de compra --> / #Compra: ${ data[0] }<!-- Número de remision -->
                            </p>
                            <p>
                                ${ formatDate( data[2] ) }<!-- fecha de registro -->
                            </p>
                        </div>                                  
                        <p class="my-2 font-bold">                                    
                            ${ data[4] }  <!-- estatus -->
                        </p>
                    </div>
                </a>     
                `;
            }
            tableBody.innerHTML = contentRows;
            const container = document.getElementById('tableRowsContainer');
            container.appendChild(tableBody);
            container.disabled = true;
            
            cardsContainer.innerHTML = contentCards;
            const containerMain = document.getElementById('mainCardsContainer');
            containerMain.appendChild(cardsContainer);
            containerMain.disabled = true;

            //Update importe chart
            const existingBarchart = document.getElementById('column-chart');
            if (existingBarchart && existingBarchart.parentNode) {
                existingBarchart.parentNode.removeChild(existingBarchart);
            }
            const newBarchart = document.createElement('div');    
            newBarchart.id = 'column-chart'
            document.getElementById('barchartContainer').appendChild(newBarchart);

            const options = {    
                series: [
                    {
                        name: "Monto",
                        color: "#db2777",
                        data: [
                        { x: "Remisionado", y: parseFloat(responseData.chartData.data[0].toFixed(2)) },                                    
                        { x: "Facturado", y: parseFloat(responseData.chartData.data[1].toFixed(2)) }
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
                chart.render()
            }            
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

const downloadPdf = async() => {
    let url;
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/pdf';
    } else {        
        url = '/registro/pdf';
    }
    
    //recollect data
    var checkboxes = document.querySelectorAll('input[type="checkbox"].btnCostumerFilter:checked');
    var valuesCostumers = Array.from(checkboxes).map(checkbox => checkbox.value);
    checkboxes = document.querySelectorAll('input[type="checkbox"].statusFilter:checked');
    var valuesStatus = Array.from(checkboxes).map(checkbox => checkbox.value);
    
    const data = { costumers : valuesCostumers,
        status: valuesStatus,
        dateStart : document.getElementById('dateStart').value,
        dateEnd : document.getElementById('dateEnd').value,
        numRemision : document.getElementById('numRemision').value,
        numCompra : document.getElementById('numCompraFilter').value };
    
    try {
        const response = await fetch(url, {            
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(new Blob([blob]));
            const a = document.createElement('a');
            a.href = url;
            a.download = 'remisiones.xlsx';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a); // Limpiar el elemento 'a' después de la descarga
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

const buttons = document.querySelectorAll('.btnCostumerFilter, .statusFilter');
buttons.forEach(boton => {
    boton.oninput = filterCostumerData;
});

document.getElementById('numRemision').oninput = filterCostumerData;
document.getElementById('numCompraFilter').oninput = filterCostumerData;

let previousValueStart = dateStart.value;
let previousValueEnd = dateEnd.value;

function checkInputChange() {
    if (dateStart.value !== previousValueStart) {
        filterCostumerData()
        previousValueStart = dateStart.value;
    }
    if (dateEnd.value !== previousValueEnd) {
        filterCostumerData()
        previousValueEnd = dateEnd.value;
    }
}

setInterval(checkInputChange, 1000);

document.getElementById('btnDownload').onclick = downloadPdf
