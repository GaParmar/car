
function post(data){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/data", true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(data));
}