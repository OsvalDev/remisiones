
//Asign functions
const switchVisible = (target) => {
    const targetObj = document.getElementById(target);

    if ( targetObj.classList.contains('invisible') ){
        targetObj.classList.remove(...['invisible','opactity-0']);
        targetObj.classList.add(...['visible', 'opacity-100']);
    }else{
        targetObj.classList.remove(...['visible', 'opacity-100']);
        targetObj.classList.add(...['invisible','opactity-0']);
    }
};


document.getElementById('btn-confirmDeliver').onclick = () => switchVisible('popover-confirmDeliver');
document.getElementById('close-confirmDeliver').onclick = () => switchVisible('popover-confirmDeliver');