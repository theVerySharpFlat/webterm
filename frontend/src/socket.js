import io from 'socket.io-client'

export let sock = io("ws://localhost:8234", {transports: ['websocket', 'polling', 'flashsocket'], reconnection: true, forceNew: false});