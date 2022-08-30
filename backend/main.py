import os, sys
import struct
import pty, fcntl, termios
import time
import array

import subprocess
import asyncio

import json


try:
    import socketio
except ModuleNotFoundError as e:
    print(f"module not found error: {e}")
    print("trying to install module...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-socketio"], check=True)
    import socketio

try:
    import uvicorn
except ModuleNotFoundError as e:
    print(f"module not found error: {e}")
    print("trying to install module...")
    subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn[standard]"], check=True)
    import uvicorn


CHILD = 0

class TTY:
    pid = None
    fd = None 

    def __init__(self):
        try:
            pid, fd = pty.fork()
        except OsError as e:
            print(f"OSError: {e}")

        if pid < 0:
            # error
            print("pty fork error!")
        elif pid == CHILD:
            sys.stdout.flush()
            try:
                env = os.environ
                #env["TERM"] = "dumb"
                os.execle("/bin/zsh", "/bin/zsh", env)
            except:
                print("execl failed!")

        else:
            self.pid = pid
            self.fd = fd

            self.resize(0, 0)

            tcattrib = termios.tcgetattr(fd)
            tcattrib[3] = tcattrib[3] & ~(termios.ICANON)
            termios.tcsetattr(fd, termios.TCSAFLUSH, tcattrib)

            
    def resize(self, cols, rows):
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))

    def write(self, bytes):
        try:
            os.write(self.fd, bytes)
        except OSError as e:
            print(f"os.write() error: {e}")
        

    def read(self):
        buf = array.array('i', [0])
        if fcntl.ioctl(self.fd, termios.FIONREAD, buf, 1) < 0:
            print("error with fcntl.ioctl(termios.FIONREAD)")
            return ""
        
        return os.read(self.fd, buf[0])
    
    def tcDrain(self):
        termios.tcdrain(self.fd)


def readSTDIN():
        buf = array.array('i', [0])
        if fcntl.ioctl(sys.stdin.fileno(), termios.FIONREAD, buf, 1) < 0:
            print("error with fcntl.ioctl(termios.FIONREAD)")
            return ""
        
        return os.read(sys.stdin.fileno(), buf[0])

server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")
app = socketio.ASGIApp(server)

connections = {}

async def ttyFN():
    while True:
        for sid, tty in connections.items():
            data = tty.read()
            if data:
                await server.emit("dat2fe", data=data, to=sid)

        await asyncio.sleep(0.01)

@server.event
async def connect(sid, environ, auth):
    print(f"connection: {sid}")
    connections[sid] = TTY()
    await server.emit("reqResz", to=sid)

@server.on("dat2be")
async def dataToBackend(sid, data):
    connections[sid].write(bytes(data, "utf-8"))

@server.on("resz")
async def reszCB(sid, data):
    obj = json.loads(data)
    cols = int(obj["cols"])
    rows = int(obj["rows"])
    connections[sid].resize(cols, rows)

@server.event
def disconnect(sid):
    print(f"disconnect: {sid}")
    connections.pop(sid)


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8234)
    # loop = asyncio.get_event_loop()
    # loop.create_task(ttyFN())
    loop = asyncio.new_event_loop()
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8234, loop=loop)
    s = uvicorn.Server(config)
    fut = loop.create_task(s.serve())
    loop.create_task(ttyFN())
    loop.run_until_complete(fut)


'''
t = TTY()
while True:
    d = t.read()
    if d:
        for byte in bytearray(d):
            print(byte, end=" ")
    t.write(readSTDIN())
    #print(repr(chr(0x0a)))
'''