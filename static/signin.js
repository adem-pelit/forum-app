var last_check = new Date().getTime()/1000
buton = document.getElementById("buton")
password = document.getElementById("pass")
nickname = document.getElementById("name")
messager = document.getElementById("messager")

change = ()=>{
    console.log(change)
}

password.addEventListener('propertychange', change);
nickname.addEventListener('propertychange', change);

function butonSetter(){
    buton.disabled = password.value.length == 8;
    console.log("disabled")
    setTimeout(butonSetter, 1000);
}

butonSetter()