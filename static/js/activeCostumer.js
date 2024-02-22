const costumerActiveData = async () => {    
    const clave = document.getElementById('clave').value;        
    const btn = document.getElementById('btnActivate');    
    const data = { numCliente : clave };
    let url =''

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/nameCostumerActive';        
    } else {        
        url = '/registro/nameCostumerActive';
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
            if (responseData.name != 'Cliente no encontrado' ){
                btn.removeAttribute("disabled");            
            }else{
                btn.setAttribute("disabled", "disabled");
            }
            document.getElementById('displayNameCostumer').textContent = responseData.name;
        }else{
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

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const responseData = await response.json();

        const containerData = document.getElementById('containerActiveCostumers');
        console.log(responseData)
        if (responseData.result === 'success') {
            let contentHTML = ""
            for (let costumer of responseData.data){
                contentHTML += ` <div class = "flex">
                    <p>${costumer[0]}</p> - <p>${costumer[1]}</p>
                </div>`
            }
            containerData.innerHTML = contentHTML;
        }else{
            containerData.innerHTML = ` <p class="w-full h-full flex justify-center items-center">Sin usuarios</p> `
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

const activateCostumer = async () => {    
    const clave = document.getElementById('clave').value;        
    const btn = document.getElementById('btnActivate');    
    const data = { numCliente : clave };
    let url =''

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        url = '/activateCostumer';        
    } else {        
        url = '/registro/activateCostumer';
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
        costumerActiveList()
        document.getElementById('clave').value = ""
        costumerActiveData()
    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

if ( document.getElementById('clave') )
    document.getElementById('clave').oninput = costumerActiveData

if ( document.getElementById('btnActivate') )
    document.getElementById('btnActivate').onclick = activateCostumer

costumerActiveData()
costumerActiveList()