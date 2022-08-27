import socket
import termios
import fcntl
import sys, os
import array

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("localhost", 8000))

while True:
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
        sock.send(data)

    def readSTDIN():
        buf = array.array('i', [0])
        if fcntl.ioctl(sys.stdin.fileno(), termios.FIONREAD, buf, 1) < 0:
            print("error with fcntl.ioctl(termios.FIONREAD)")
            return ""
        
        return os.read(sys.stdin.fileno(), buf[0])
    
    os.write(sys.stdout.fileno(), readSocket())
    writeSocket(readSTDIN())