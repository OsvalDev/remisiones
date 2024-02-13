
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

if (document.getElementById('btn-confirmDeliver'))
    document.getElementById('btn-confirmDeliver').onclick = () => switchVisible('popover-confirmDeliver');

if (document.getElementById('close-confirmDeliver'))
    document.getElementById('close-confirmDeliver').onclick = () => switchVisible('popover-confirmDeliver');

//Logistic
if (document.getElementById('btn-endConfirmLog'))
    document.getElementById('btn-endConfirmLog').onclick = () => switchVisible('popover-endConfirmLog');

if (document.getElementById('close-endConfirmLog'))
    document.getElementById('close-endConfirmLog').onclick = () => switchVisible('popover-endConfirmLog');

if (document.getElementById('btn-endLog'))
    document.getElementById('btn-endLog').onclick = () => switchVisible('popover-endLog');

if (document.getElementById('close-endLog'))
    document.getElementById('close-endLog').onclick = () => switchVisible('popover-endLog');

if (document.getElementById('btn-chofer'))
    document.getElementById('btn-chofer').onclick = () => switchVisible('popover-chofer');

if (document.getElementById('close-chofer'))
    document.getElementById('close-chofer').onclick = () => switchVisible('popover-chofer');

//surtiment
if (document.getElementById('btn-endConfirmSur'))
    document.getElementById('btn-endConfirmSur').onclick = () => switchVisible('popover-endConfirmSur');

if (document.getElementById('close-endConfirmSur'))
    document.getElementById('close-endConfirmSur').onclick = () => switchVisible('popover-endConfirmSur');

if (document.getElementById('btn-endSur'))
    document.getElementById('btn-endSur').onclick = () => switchVisible('popover-endSur');

if (document.getElementById('close-endSur'))
    document.getElementById('close-endSur').onclick = () => switchVisible('popover-endSur');

if (document.getElementById('btn-autorization'))
    document.getElementById('btn-autorization').onclick = () => switchVisible('popover-autorization');

if (document.getElementById('close-autorization'))
    document.getElementById('close-autorization').onclick = () => switchVisible('popover-autorization');