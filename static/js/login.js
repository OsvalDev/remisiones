import utils from './utils.js';
const btnToken = document.getElementById('btnLogin');

const login = async () => {    
    const id = document.getElementById('idWorker').value;
    const psw = document.getElementById('password').value;

    if (id == '' || psw == '') {        
        utils.removeElement('noti');
        utils.makeAlert('Llene todos los campos requeridos', 'loginContainer');
        return;
    }

    const data = { id, psw };

    const url = '/registro/login';
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

        if (responseData.result === 'failed') {
            utils.removeElement('noti');
            utils.makeAlert(responseData.msg, 'loginContainer');
        }else{
            window.location.href = "/registro/dashboard";
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

btnToken.onclick = login;
