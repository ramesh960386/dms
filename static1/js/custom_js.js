/*
document.onmousedown = disableRightclick;
var message = "Right click not allowed !!";
function disableRightclick(evt){
    if(evt.button == 2){
        alert(message);
        return false;
    }
}
*/
//////////////////////
myFile = document.getElementById("myFile")
btn = document.getElementById("myBtn")
btn.addEventListener("click", function() {
    url = myFile.href
    fetch(url, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    });
});