import io from 'socket.io-client'

let PORT = 0

let xhr = new XMLHttpRequest();
xhr.open('GET', '/backend-config.json', false);


xhr.onload = function() {
  if (xhr.status != 200) { // analyze HTTP status of the response
    alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
  } else { // show the result
    let json = JSON.parse(xhr.responseText);
    console.log("port: " + json["port"])
    PORT = json["port"];
  }
};


xhr.onerror = function() {
  alert("failed to load settings!");
};
xhr.send();

export let sock = io("ws://localhost:" + PORT, {transports: ['websocket', 'polling', 'flashsocket'], reconnection: true, forceNew: false});