// alert()

document.getElementById("GetUserNameBtn").addEventListener("click",()=>{
    document.getElementById("loader-container").classList.add("display-flex");
    var userName = document.getElementById("userName").value;
    setTimeout(()=>{window.location.href = `/api/twitter/username=${userName}`},100);
});
document.getElementById("GetUserNameBtn-main").addEventListener("click",()=>{
    document.getElementById("loader-container").classList.add("display-flex");
});