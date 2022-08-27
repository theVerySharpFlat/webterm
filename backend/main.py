import os, sys
import struct
import pty, fcntl, termios
import time
import array

import socket
import threading

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

def handleConnection(sock: socket.socket):
    t = TTY()
    sock.setblocking(False)
    def readSocket() -> bytes:
        output = b""
        buf = array.array("i", [0])
        while True:
            if fcntl.ioctl(sock.fileno(), termios.FIONREAD, buf, 1) < 0:
                print("failed to fionread")
                return b""
            if buf[0] == 0:
                return output
            try:
                output += sock.recv(buf[0])
            except socket.error as e:
                print("socket error:", e)
                return b""
    
    def writeSocket(data: bytes):
        try:
            sock.sendall(data)
        except socket.error as e:
            print("socket error:", e)
            print("possibly disconnected?")

    while True:
        readBytes = readSocket()
        t.write(readBytes)
        writeSocket(t.read())
    pass

class SocketManager:
    socket = None
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", 8000))
        self.socket.listen(1)
    
    def accept(self):
        (clientSocket, address) = self.socket.accept()
        thread = threading.Thread(target=handleConnection, args=(clientSocket,), daemon=True)
        thread.run()


def readSTDIN():
        buf = array.array('i', [0])
        if fcntl.ioctl(sys.stdin.fileno(), termios.FIONREAD, buf, 1) < 0:
            print("error with fcntl.ioctl(termios.FIONREAD)")
            return ""
        
        return os.read(sys.stdin.fileno(), buf[0])

sm = SocketManager()
sm.accept()

while True:
    time.sleep(1)
# while True:
#     t.write(readSTDIN())
#     t.tcDrain()
#     try:
#         os.write(sys.stdout.fileno(), t.read())
#     except OSError as e:
#         print(f"os.write(): {e}")
#     sys.stdout.flush() 