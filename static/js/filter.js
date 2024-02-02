const formatDate = (fechaString) => {
    const fecha = new Date(fechaString);
    const fechaFormateada = fecha.toISOString().split('T')[0];
    return fechaFormateada
}

const filterCostumerData = async (element) => {
    let url;
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/getRemissionByCostumer/';
    } else {        
        url = '/registro/getRemissionByCostumer/';
    }    

    try {
        const response = await fetch(url + element.value , {            
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
            console.log(responseData.data)
            const existingAlert = document.getElementById('tableRows');
            if (existingAlert && existingAlert.parentNode) {
                existingAlert.parentNode.removeChild(existingAlert);
            }

            const tableBody = document.createElement('tbody');            
            tableBody.id = 'tableRows';
            
            let contentRows = '';
            for (let data of responseData.data){                
                contentRows += `
                    <tr  class="bg-white border-b hover:bg-gray-50" >
                        <td scope="row" class=" w-20 px-6 py-4">
                            <a href="remission/${ data[0] }/${ data[1] }">
                                ${ data[1] }  <!-- Número de compra -->
                            </a>                                        
                        </td>
                        <td class="w-20 px-6 py-4">
                            <a href="remission/${ data[0] }/${ data[1] }">
                                ${ data[0] }<!-- Número de remision -->
                            </a>                                        
                        </td>
                        <td class="w-40 px-6 py-4">
                            <a href="remission/${ data[0] }/${ data[1] }">
                                ${ formatDate( data[2] ) }<!-- fecha de registro -->
                            </a>                                        
                        </td>
                        <td class="w-80 px-6 py-4">
                            <a href="remission/${ data[0] }/${ data[1] }">
                                ${ data[3] }  <!-- cliente -->
                            </a>                                        
                        </td>                                
                        <td class="w-40 px-6 py-4">
                            <a href="remission/${ data[0] }/${ data[1] }">
                                ${ data[4] }  <!-- estatus -->
                            </a>
                        </td>                                
                    </tr>                                
                `;
            }
            tableBody.innerHTML = contentRows;
            const container = document.getElementById('tableRowsContainer');
            container.appendChild(tableBody);
            container.disabled = true;
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

const buttons = document.querySelectorAll('.btnCostumerFilter');
buttons.forEach(boton => {
    boton.onclick = function() {
        filterCostumerData(this);
    };
});

