const nameCostumer = async () => {    
    const numCliente = document.getElementById('numCliente').value;        

    const data = { numCliente };
    let url =''

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/nameCostumer';        
    } else {        
        url = '/registro/nameCostumer';
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
            document.getElementById('nameCostumerView').textContent = responseData.name;

            if (responseData.name != 'Cliente no encontrado'){
                document.getElementById('btnSubmit').removeAttribute("disabled");
            }else{
                document.getElementById('btnSubmit').setAttribute("disabled", "disabled");
            }
                
        }else{
            console.log(responseData.name);
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

document.getElementById('numCliente').oninput = nameCostumer