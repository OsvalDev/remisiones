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
    const urls = {
        login: '',
        dashboard: ''
    }

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        urls.login = '/loginCostumer';
        urls.dashboard = '/cliente/dashboard';
    } else {        
        urls.login = '/registro/loginCostumer';
        urls.dashboard = '/registro/cliente/dashboard';
    }
    const body = data;

    try {
        const response = await fetch(urls.login, {
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
            window.location.href = urls.dashboard;
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

btnToken.onclick = login;
