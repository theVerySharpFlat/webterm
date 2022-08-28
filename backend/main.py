import os, sys
import struct
import pty, fcntl, termios
import time
import array

import subprocess

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
                os.execle("/bin/sh", "/bin/sh", env)
            except:
                print("execl failed!")

        else:
            fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 900, 900, 0, 0))

            tcattrib = termios.tcgetattr(fd)
            tcattrib[3] = tcattrib[3] & ~(termios.ICANON | termios.ECHO | termios.ECHONL)
            termios.tcsetattr(fd, termios.TCSAFLUSH, tcattrib)

            self.pid = pid
            self.fd = fd
            
            # os.write(sys.stdout.fileno(), os.read(fd, 1024))
            # os.write(fd, b"echo hello\n")
            # time.sleep(3)
            # os.write(sys.stdout.fileno(), os.read(fd, 2048))

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

@server.event
async def connect(sid, environ, auth):
    print(f"connection: {sid}")
    await server.emit("message", "Hello, World!")

@server.event
def disconnect(sid):
    print(f"disconnect: {sid}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8234)