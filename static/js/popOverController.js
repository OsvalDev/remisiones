
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

//Logistic
document.getElementById('btn-endConfirmLog').onclick = () => switchVisible('popover-endConfirmLog');
document.getElementById('close-endConfirmLog').onclick = () => switchVisible('popover-endConfirmLog');
document.getElementById('btn-endLog').onclick = () => switchVisible('popover-endLog');
document.getElementById('close-endLog').onclick = () => switchVisible('popover-endLog');

//surtiment
document.getElementById('btn-endConfirmSur').onclick = () => switchVisible('popover-endConfirmSur');
document.getElementById('close-endConfirmSur').onclick = () => switchVisible('popover-endConfirmSur');
document.getElementById('btn-endSur').onclick = () => switchVisible('popover-endSur');
document.getElementById('close-endSur').onclick = () => switchVisible('popover-endSur');