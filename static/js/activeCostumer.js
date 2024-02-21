const costumerActiveData = async () => {    
    const clave = document.getElementById('clave').value;        
    const inputClave = document.getElementById('clave');
    const data = { clave };
    let url =''

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/costumerActiveData';        
    } else {        
        url = '/registro/costumerActiveData';
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
            inputClave.removeAttribute("disabled");
        }else{
            inputClave.setAttribute("disabled", "disabled");
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

const costumerActiveList = async () => {    
    let url =''

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/costumerActiveList';        
    } else {        
        url = '/registro/costumerActiveList';
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
            inputClave.removeAttribute("disabled");
        }else{
            
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

if ( document.getElementById('clave') )
    document.getElementById('clave').oninput = costumerActiveData
