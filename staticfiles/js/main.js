// alert()
// const addActiveClassSelector = (id) => {
//     var checkClassList = document.getElementById(id).classList;
//     checkClassList.contains("active-selector") ? checkClassList.remove("active-selector") : checkClassList.add("active-selector");

//     var classLen = document.getElementsByClassName("social-selector");
//     for (var i=0;i<=1;i++){
//         if (classLen[i].classList.contains("active-selector")){
//             document.getElementById("proceed-btn").classList.add("proceed-active");
//             return null;
//         }
//         else{
//             document.getElementById("proceed-btn").classList.remove("proceed-active");
//         }
//     }
// }

// document.getElementById("proceed-btn").addEventListener("click",()=>{
//     var classLen = document.getElementsByClassName("social-selector");
//     for (var i=0;i<=1;i++){
//         if (classLen[i].classList.contains("active-selector")){
//             alert();
//             return null;
//         }
//         else{
//             console.log("hi");
//         }
//     }
// });

const addActiveClassSelector = (id) => {
    for (var i=0;i<=1;i++){
        document.getElementsByClassName("social-selector")[i].classList.remove("active-selector");
    }
    document.getElementById(id).classList.add("active-selector");
    document.getElementById("proceed-btn-prev").style.display="none";
    document.getElementById("proceed-btn").style.display="block";
    if(id === "twitter-selector"){
        document.getElementById("submit-val").value = "twitter";
    }
    else if(id === "facebook-selector"){
        document.getElementById("submit-val").value = "facebook";
    }
}