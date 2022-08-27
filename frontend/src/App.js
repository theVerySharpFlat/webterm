import React from 'react'
import './App.css';

import { Terminal } from 'xterm'
import 'xterm/css/xterm.css'
//import { FitAddon } from 'xterm-addon-fit'

class App extends React.Component {
  constructor() {
    super()
    this.terminal = new Terminal();
    // this.fitAddon = new FitAddon();
    this.initializedTerminal = false;
  }

  componentDidMount() {
    if(!this.initializedTerminal) {
      this.terminal.open(document.getElementById("terminal"))
      //this.terminal.loadAddon(this.fitAddon);
      //this.fitAddon.fit();
      this.terminal.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ')
      this.initializedTerminal = true;
    }
  }

  render() {
    return <div id="terminal"></div>
  }
}

export default App;
