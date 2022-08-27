import React from 'react'
import './App.css';

import { Terminal } from 'xterm'
import 'xterm/css/xterm.css'
import { FitAddon } from 'xterm-addon-fit'

let fitFN = null;

class App extends React.Component {
  constructor() {
    super()
    this.terminal = new Terminal();
    this.terminal.onResize(evt => {
      console.log(`resize: (${evt.cols}, ${evt.rows})`);
    });
    this.fitAddon = new FitAddon();
    fitFN = () => {
      this.fitAddon.fit();
    }
    window.onresize = function() {
      fitFN();
    }
    this.initializedTerminal = false;

    this.socket = new WebSocket("https://8000-theverysharpfla-webterm-dtom034vv3a.ws-us63.gitpod.io/");
    this.socket.addEventListener("message", message => {
      console.log("message from server: " + message.data);
    });
  }

  componentDidMount() {
    if(!this.initializedTerminal) {
      this.terminal.open(document.getElementById("terminal"))
      this.terminal.loadAddon(this.fitAddon);
      this.fitAddon.fit();
      this.terminal.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ')
     
      this.initializedTerminal = true;
    }
  }

  render() {
    return <div id="terminal"></div>
  }
}

export default App;
