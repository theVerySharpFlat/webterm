import React from 'react'
import './App.css';

import { Terminal } from 'xterm'
import 'xterm/css/xterm.css'
import { FitAddon } from 'xterm-addon-fit'

import {sock} from './socket'

let fitFN = null;



class App extends React.Component {
  constructor() {
    super()
    this.terminal = new Terminal({
      fontFamily: "JetBrains Mono"
    });
    this.terminal.onResize(evt => {
      console.log(`resize: (${evt.cols}, ${evt.rows})`);
    });
    this.fitAddon = new FitAddon();
    fitFN = () => {
      this.fitAddon.fit();
      sock.emit("resz", JSON.stringify({
        "rows": this.terminal.rows,
        "cols": this.terminal.cols
      }));
    }
    window.onresize = function() {
      fitFN();
    }
    this.initializedTerminal = false;

    sock.once("connect", () => {
      console.log("connected to " + sock.id);
    });

    sock.on("dat2fe", (data) => {
      this.terminal.write(new Uint8Array(data));
    });

    sock.on("reqResz", (data) => {
      console.log("requestResize")
      fitFN();
    });

    this.terminal.onData(recv => sock.emit("dat2be", recv));

    sock.once("disconnect", () => {
      console.log("disconnected from " + sock.id);
    });

  }

  componentDidMount() {
    if(!this.initializedTerminal) {
      this.terminal.open(document.getElementById("terminal"))
      this.terminal.loadAddon(this.fitAddon);
      this.fitAddon.fit();
     
      this.initializedTerminal = true;
    }
  }

  render() {
    return (
      <div id="terminal"></div>
    )
  }
}

export default App;
