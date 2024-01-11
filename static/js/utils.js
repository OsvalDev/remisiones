const utils = {};

utils.makeAlert = (msg, containerId) => {    
    const alertDiv = document.createElement('div');
    alertDiv.className = 'flex items-center p-4 my-4 text-sm text-red-800 rounded-lg bg-red-50 animate__bounceIn';
    alertDiv.role = 'alert';
    alertDiv.id = 'noti'
    alertDiv.innerHTML = `
        <svg class="flex-shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
        </svg>
        <span class="sr-only">Info</span>
        <div>
            <span class="font-medium">Mensaje: </span> ${msg}
        </div>
    `;
    
    document.getElementById(containerId).appendChild(alertDiv);
}

utils.removeElement = (id) => {
    const existingAlert = document.getElementById(id);
    if (existingAlert && existingAlert.parentNode) {
        existingAlert.parentNode.removeChild(existingAlert);
    }
};

export default utils;