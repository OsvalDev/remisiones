const showPsw = () => {
    const ojito = document.getElementById('ojito')
    const psw = document.getElementById('password')

    if (psw.type === "password"){
        psw.type = "text";
        ojito.classList.remove('bx-show');
        ojito.classList.add('bxs-hide');
    }else{
        psw.type = "password";
        ojito.classList.remove('bxs-hide');
        ojito.classList.add('bx-show');
    }
}

document.getElementById('ojito').onclick = showPsw;