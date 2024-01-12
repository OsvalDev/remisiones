import utils from './utils.js';
const btnsync = document.getElementById('btnsync');

const sync = async () => {    

    utils.removeElement('syncText');
    utils.showSync( 'btnsync');
    
    const urls = {
        sync: '',
        costumers: ''
    }

    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {        
        urls.sync = '/sync';
        urls.costumers = '/costumers';
    } else {        
        urls.sync = '/registro/sync';
        urls.costumers = '/registro/costumers';
    }    

    try {
        const response = await fetch(urls.sync, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const responseData = await response.json();        
        
        if (responseData.result === 'failed') {
            utils.removeElement('noti');
            utils.makeAlert(responseData.msg, 'syncContainer');
        }else{
            window.location.href = urls.costumers;
        }

    } catch (err) {
        console.log('Error en la solicitud: ', err.message);
    }
};

btnsync.onclick = sync;
