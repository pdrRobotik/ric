
var _ws = null; 

function AN_setup(addr,port=5678,mode="w",name=(((Date.now()/1000)|0)%10000),callback = (evt) => {var received_msg = evt.data; alert(received_msg);}) { //mode: w/n 
    if ("WebSocket" in window) {
        _ws = new WebSocket("ws://"+addr+":"+port);
        _ws.onopen = function() { _ws.send(name+":"+mode); };
        _ws.onmessage = callback;
        _ws.onclose = function() { alert("Connection is closed...");};
    } else {
        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
    }
}

function AN_send(target,targetgroup,message) {
    _ws.send(target+"@"+targetgroup+":"+message)
}
