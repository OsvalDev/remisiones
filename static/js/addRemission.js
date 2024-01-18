const newRemission = async () => {        

    const numCompra = document.getElementById('numCompra');
    const numRemission = document.getElementById('numRemission');
    const numCliente = document.getElementById('numCliente');
    const piezas = document.getElementById('piezas');
    const remisionado = document.getElementById('remisionado');
    const facturado = document.getElementById('facturado');

    const data = {
            numCompra : numCompra.value,
            numRemission : numRemission.value,
            numCliente : numCliente.value,
            piezas : piezas.value,
            remisionado : remisionado.value,
            facturado : facturado.value
    }
    
    let url =''

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/newRemission';        
    } else {        
        url = '/registro/newRemission';
    }
    const body = data;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const responseData = await response.json();

        if (responseData.result === 'success') {
            numRemission.value = ''            
            piezas.value = ''
            remisionado.value = ''
            facturado.value = ''
        }else{
            alert('Hubo un error en la base de datos')
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};


const refreshPage = () => window.location.href = '/registro/dashboard';

const getTotalMount = () => {
    const facturado = document.getElementById('facturado').value;
    const remisionado = document.getElementById('remisionado').value;
    const total = document.getElementById('total');

    let totalMount = 0;
    if (facturado != '')   totalMount += parseInt(facturado);
    if (remisionado != '')   totalMount += parseInt(remisionado);
1
    total.textContent = `Total ${totalMount}`
}

document.getElementById('btnSubmit').onclick = newRemission;
document.getElementById('btnClose').onclick = refreshPage;
document.getElementById('facturado').oninput = getTotalMount;
document.getElementById('remisionado').oninput  = getTotalMount;