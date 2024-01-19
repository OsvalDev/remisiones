const newRemission = async () => {        

    const numCompra = document.getElementById('numCompra');
    const numRemission = document.getElementById('numRemission');
    const numCliente = document.getElementById('numCliente');
    const piezas = document.getElementById('piezas');
    const remisionado = document.getElementById('remisionado');
    const facturado = document.getElementById('facturado');
    const bonificado = document.getElementById('bonificado');

    const data = {
            numCompra : numCompra.value,
            numRemission : numRemission.value,
            numCliente : numCliente.value,
            piezas : piezas.value,
            remisionado : remisionado.value,
            facturado : facturado.value,
            bonificado : bonificado.value
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
            bonificado.value = ''
            document.getElementById('total').textContent = 'Total: $ 0.0'
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

    let totalMount = 0.0;
    if (facturado != '')   totalMount += parseFloat(facturado);
    if (remisionado != '')   totalMount += parseFloat(remisionado);

    total.textContent = `Total: $ ${totalMount}`
}

const btnSubmit = document.getElementById('btnSubmit');
if (btnSubmit) btnSubmit.onclick = newRemission;

const btnClose = document.getElementById('btnClose');
if (btnClose) btnClose.onclick = refreshPage;

document.getElementById('facturado').oninput = getTotalMount;
document.getElementById('remisionado').oninput  = getTotalMount;

getTotalMount()